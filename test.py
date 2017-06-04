from firebase import firebase
import subprocess
firebase = firebase.FirebaseApplication('https://hotmelon-655ec.firebaseio.com', None)
ppt = '/ppt_test'
post_content = "{'title': "+"title}"
post_cmd = ['curl', '-X', 'POST', '-d', post_content, 'https://hotmelon-655ec.firebaseio.com/ppt.json']

subprocess.check_output(post_cmd, stderr=subprocess.STDOUT)