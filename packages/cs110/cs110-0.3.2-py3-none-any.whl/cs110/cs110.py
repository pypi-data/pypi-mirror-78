import __main__ as main
import os, sys, requests

# ---------------------------------------------------------------------
# CS110 Autograder Code (Client i.e., Student Side)
# These functions are used to contact the server
# ---------------------------------------------------------------------

# Constants
autograder_version = 1.0
autograder_ping = "https://autograder.net/ping.php"
autograder_url  = "https://autograder.net/get_testcase.php"

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
    except Exception as e:
        pass
    
    return False


# Determines if the User would like to run the autograder
def get_user_preference():
    global connected, debug
    
    print("---------------------------------------------------")
    print("# File:", filename)
    print("---------------------------------------------------")
    
    # Automatically Turns off the Autograder if we are Not Connected to the Internet
    if connected:
        user_input = input("Test against server? [Y/N]: ")
        user_input = user_input.strip().lower()
    else:
        print("Not connected to Internet.  Running program locally.")
        user_input = 'n'
    print()
    
    if user_input == 'y' or user_input == 'yes':
        return True
    elif user_input == 'debug':
        debug = True
        return True
    
    return False


# -------------------------------------------------------
# Main Code
# -------------------------------------------------------
if '__ignore__' not in sys.argv:
    
    # Checks to See if we are Connected to the Internet
    connected = connected_to_internet()
    
    # Determines if the User wants to grade the program, or just run it
    run_autograder = get_user_preference()

    # Contacts the API and gets the response
    try:
        if debug or run_autograder == True:
            print("Running Autograder (Version " + str(autograder_version) + ")")
            print("Contacting Test Server . . . ", end='')
        
        # Generates the Post Data
        post_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        post_data = { "user":os.getlogin(), "filename":filename, "filepath":file_path, "code":file_contents, "language":"python", "autograde":run_autograder, "version":autograder_version }
        response = requests.post(autograder_url, data=post_data, headers=post_headers)
        response_json = response.json()
        
        if debug or run_autograder == True:
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
            exit()

    if run_autograder == True:
        # Converts the (text) Response to a Dictionary
        try:
            # Extracts the Response Code and Message
            response_code = int(response_json['response_code'])
            response_message = response_json['message']
            response_timestamp = int(response_json['timestamp'])
                
            if response_code == 200:
                exec(compile(source=response_message, filename='unittest.py', mode='exec'))
                run_testcases(response_json)
            elif response_code == 505:
                print("Autograder Version Not Supported")
                print("Update the CS110 module and try again (in Thonny, go to tools -> manage plug-ins)")
            else:
                print("Response Code:", response_code)
                print(" ", response_message)
            
        except Exception as e:
            print("Unexpected Error:", e)

        # Prevents Your Program from Running a Second Time
        exit()

