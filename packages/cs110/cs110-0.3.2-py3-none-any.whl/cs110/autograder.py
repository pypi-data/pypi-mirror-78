import __main__ as main

import getpass
import hashlib
import os
import py_compile
import requests
import shutil
import subprocess
import sys


# ---------------------------------------------------------------------
# CS110 Autograder Code (Client i.e., Student Side)
# These functions are used to contact the server
# ---------------------------------------------------------------------

# Constants
autograder_version = 0.32
autograder_ping = "https://autograder.dfcs-cloud.net/versioninfo.php"
autograder_url = "https://autograder.dfcs-cloud.net/get_testcase.php"
scoring_url = "https://autograder.dfcs-cloud.net/upload_result.php"
grades_url = "https://autograder.dfcs-cloud.net/reports.php"

# Grabs the Contents of the Program that Called It
filename = main.__file__
file = open(filename, "r")
file_path = os.path.abspath(filename)
file_contents = file.read()
debug = False


# Determines if the Device is Connected to the Internet
def connected_to_internet():
    try:
        _ = requests.get(autograder_ping, timeout=3)
        return True
    except Exception:
        pass

    return False


# Determines if the User would like to run the autograder
def get_user_preference():
    global connected, debug

    print("---------------------------------------------------")
    print("# File:", filename)
    print("---------------------------------------------------")

    # Automatically Turns off the Autograder if we are Not Connected to the
    # Internet
    if connected:
        user_input = input("Test against server? [Y/N]: ")
        user_input = user_input.strip().lower()
    else:
        print("Cannot connect to autograder website.  Running program locally.")
        user_input = 'n'
    print()

    if user_input == 'y' or user_input == 'yes':
        return True
    elif user_input == 'debug':
        debug = True
        return True

    return False


# Get the current user
def _get_login():
    username = None
    try:
        username = os.getlogin()
    except OSError:
        username = getpass.getuser()

    return username


# -------------------------------------------------------------
# Extracts Inputs from a List
# -------------------------------------------------------------
def get_inputs(input_list):
    result = ""
    for i in input_list:
        result += str(i) + "\n"
    return result


# -------------------------------------------------------------
# Runs a Python script and returns any output and/or errors
# -------------------------------------------------------------
def run_script(filename, input_list=[], print_details=True,
               timeout_in_seconds=5):
    # Prints out the Program's Input(s)
    if print_details and len(input_list) > 0:
        print("Inputs Provided:")
        for item in input_list:
            print(str(item))
        print()

    input_bytes = get_inputs(input_list)

    try:
        p = subprocess.Popen([sys.executable, filename],
                             universal_newlines=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=dict(os.environ, DISABLE_AUTOGRADER='1'))
        out, err = p.communicate(input=input_bytes, timeout=timeout_in_seconds)
    except subprocess.TimeoutExpired:
        out = ''
        err = ('Timed out after ' + str(timeout_in_seconds) + ' seconds.  '
               'This occurs when your program asks for more inputs than the '
               'test case provides, or when you have a loop that does not '
               'end.')

    # Prints out the Program's Output
    if print_details:
        print("Your Program's Output:")
        if out != '':
            print(out)
        else:
            print("No Output Produced\n")

    # Displays the Error Message (if one is provided)
    if print_details and err != '':
        print("Error Occurred:")
        print(err)
        print()

    if print_details:
        print("Feedback:")

    return (out, err)


# -------------------------------------------------------------
# Reports the Results of the Test, and Removes any Extra Files
# -------------------------------------------------------------
def cleanup(filename, testcase_response_json, points_earned):
    # Gets Information Needed from the Testcase Webservice
    timestamp = int(testcase_response_json['timestamp'])

    # Sends the Results of the Test Back to the Server for Archiving
    post_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; '
                                  'Intel Mac OS X 10_10_1) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/39.0.2171.95 Safari/537.36'}
    post_data = {
        "user": _get_login(),
        "filename": filename,
        "filepath": file_path,
        "score": points_earned,
        "language": "python",
        "timestamp": timestamp,
    }
    response = requests.post(scoring_url, data=post_data, headers=post_headers)
    response_json = response.json()
    response_code = int(response_json['response_code'])

    if response_code == 200:
        print("\nScore:", str(points_earned) + "%")
        print("To View Your Performance on Programming Assignments, Go To: ")
        user_hash = hashlib.sha1(_get_login().encode('utf-8'))
        print(grades_url + "?course=1&id=" + str(user_hash.hexdigest()))
    else:
        print(response.text)

    # Removes the pycache folder
    if os.path.isdir('__pycache__'):
        shutil.rmtree("__pycache__")


# -------------------------------------------------------------
# Executes the Test Cases
# -------------------------------------------------------------
def run_testcases(test_passed, testcase_response_json, perform_cleanup=True):
    points_earned = test_passed()

    if perform_cleanup:
        cleanup(filename, testcase_response_json, points_earned)

    return points_earned


# -------------------------------------------------------------
# UNIT TEST FUNCTION
# Determines if the Python file provided would run (does not actually run it)
# -------------------------------------------------------------
def code_compiles(filename):
    try:
        py_compile.compile(filename, doraise=True)
        return True
    except Exception:
        return False


# -------------------------------------------------------------
# UNIT TEST FUNCTION
# Determines if two values are numerically equivalent
# -------------------------------------------------------------
def equals(value, expected_value, delta=0.01):
    try:
        return (float(value) >= float(expected_value) - delta and
                float(value) <= float(expected_value) + delta)
    except Exception:
        return False


# -------------------------------------------------------------
# UNIT TEST FUNCTION
# Compares two lists of strings to see if they equal
# -------------------------------------------------------------
def compare_strings(student_output_list, expected_output_list, auto_trim=True,
                    check_order=True):
    num_matches = 0

    for i in range(len(student_output_list)):
        print("Line " + str(i+1) + ": ", end='')
        if i < len(expected_output_list):
            if auto_trim:
                student_output_list[i] = student_output_list[i].strip()
                expected_output_list[i] = expected_output_list[i].strip()
            if student_output_list[i] == expected_output_list[i]:
                print("CORRECT")
                num_matches += 1
            else:
                print("INCORRECT (Expected: '{}')".format(expected_output_list[i]))
        else:
            print("INCORRECT (Unexpected Line: '{}')".format(student_output_list[i]))

    print(num_matches, "out of", len(expected_output_list), "lines match")

    return num_matches


# -------------------------------------------------------
# Main Code
# -------------------------------------------------------
def main():
    global connected, debug

    # Checks to See if we are Connected to the Internet
    connected = connected_to_internet()

    # Determines if the User wants to grade the program, or just run it
    run_autograder = get_user_preference()

    # Contacts the API and gets the response
    try:
        if debug or run_autograder:
            print("Running Autograder (Version " +
                  str(autograder_version) + ")")
            print("Contacting Test Server . . . ", end='')

        # Generates the Post Data
        post_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; '
                                      'Intel Mac OS X 10_10_1) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/39.0.2171.95 Safari/537.36'}
        post_data = {"user": _get_login(),
                     "filename": filename,
                     "filepath": file_path,
                     "code": file_contents,
                     "language": "python",
                     "autograde": run_autograder,
                     "version": autograder_version,
                     }
        response = requests.post(autograder_url, data=post_data, headers=post_headers)
        response_json = response.json()

        if debug or run_autograder:
            print("SUCCESS!\n")

        # Debug
        if debug:
            print("Debug Information: ")
            print(response.text)
            print()

    except Exception as e:
        if connected and (debug or run_autograder):
            print("PROBLEM ENCOUNTERED")
            print(e)
            print(response.text)
            sys.exit()

    if run_autograder:
        # Converts the (text) Response to a Dictionary
        try:
            # Extracts the Response Code and Message
            response_code = int(response_json['response_code'])
            response_message = response_json['message']

            if response_code == 200:
                namespace = globals()
                exec(compile(source=response_message, filename='<string>',
                             mode='exec'), namespace)
                test_passed = namespace['test_passed']
                run_testcases(test_passed, response_json)
            elif response_code == 505:
                print("Autograder Version Not Supported")
                print("Update the CS110 module and try again "
                      "(in Thonny, go to tools -> manage plug-ins)")
            else:
                print("Response Code:", response_code)
                print(" ", response_message)

        except Exception as e:
            print("Unexpected Error:", e)

        # Prevents Your Program from Running a Second Time
        sys.exit()


if '_test.py' not in filename and 'DISABLE_AUTOGRADER' not in os.environ:
    main()
