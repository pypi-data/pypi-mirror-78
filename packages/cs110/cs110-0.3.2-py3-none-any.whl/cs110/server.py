import requests
import subprocess, sys, os, shutil, hashlib, py_compile

from cs110 import client

# ---------------------------------------------------------------------
# CS110 Autograder Code (Server Side)
# These functions are downloaded to the client to perform autograding
# ---------------------------------------------------------------------
scoring_url = "https://www.autograder.net/upload_result.php"
grades_url  = "https://www.autograder.net/reports.php"


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
def run_script(filename, input_list = [], print_details=True, timeout_in_seconds=5):
    # Prints out the Program's Input(s)
    if print_details and len(input_list) > 0:
        print("Inputs Provided:")
        for item in input_list:
            print(str(item))
        print()
    
    input_bytes = get_inputs(input_list)
    
    try:
        p = subprocess.Popen(['python', filename, '__ignore__'], universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=dict(os.environ, DISABLE_AUTOGRADER='1'))
        out, err = p.communicate(input=input_bytes, timeout=timeout_in_seconds)
    except subprocess.TimeoutExpired:
        out = ''
        err = 'Timed out after ' + str(timeout_in_seconds) + ' seconds.  This happens when your program asks for more inputs than the test case provides, or when you have a loop that does not end.'
    
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
    post_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    post_data = { "user":os.getlogin(), "filename":filename, "filepath":client.file_path, "score":points_earned, "language":"python", "timestamp":timestamp }
    response = requests.post(scoring_url, data=post_data, headers=post_headers)
    response_json = response.json()
    response_code = int(response_json['response_code'])
        
    if response_code == 200:
        print("\nScore:", str(points_earned) + "%")
        print("To View Your Performance on Programming Assignments, Go To: ")
        user_hash = hashlib.sha1(os.getlogin().encode('utf-8'))
        print(grades_url + "?id=" + str(user_hash.hexdigest()))
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
        cleanup(client.filename, testcase_response_json, points_earned)
    
    return points_earned


# -------------------------------------------------------------
# UNIT TEST FUNCTION
# Determines if the Python file provided would run (does not actually run it)
# -------------------------------------------------------------
def code_compiles(filename):
    try:       
        py_compile.compile(filename, doraise=True)
        return True
    except:
        return False

# -------------------------------------------------------------
# UNIT TEST FUNCTION
# Determines if two values are numerically equivalent
# -------------------------------------------------------------
def equals(value, expected_value, delta = 0.01):
    try:
        return float(value) >= float(expected_value) - delta and float(value) <= float(expected_value) + delta
    except:
        return False
    
    
# -------------------------------------------------------------
# UNIT TEST FUNCTION
# Compares two lists of strings to see if they equal
# -------------------------------------------------------------
def compare_strings(student_output_list, expected_output_list, auto_trim=True, check_order=True):
    num_matches = 0
    
    for i in range(len(student_output_list)):
        print("Line " + str(i+1) + ": ", end='')
        if i < len(expected_output_list):
            if auto_trim == True:
                student_output_list[i] = student_output_list[i].strip()
                expected_output_list[i] = expected_output_list[i].strip()
            if student_output_list[i] == expected_output_list[i]:
                print("CORRECT")
                num_matches += 1
            else:
                print("INCORRECT (Expected: '" + str(expected_output_list[i]) + "')", student_output_list[i])
        else:
            print("INCORRECT (Unexpected Line: '" + str(student_output_list[i]) + "')")
    
    print(num_matches, "out of", len(expected_output_list), "lines match")
    
    return num_matches


# Helper Console for Outputting
class Console:
    def write(self, txt):
        print(str(txt), end='')
