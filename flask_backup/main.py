import os
import urllib.request
from app import app
from facade import INPUTPATH, THRESHOLD, video_process
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['mp4', 'mov', 'mxf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_form():
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST']) #exapting POST request from upload-button from index.html
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file')
			return redirect('/')
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for upload')
			return redirect('/')
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			INPUTPATH = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/analysis')
		else:
			flash('Allowed file types are mp4, mov, mxf, png, jpg, gif')
			return redirect('/')

@app.route('/analysis')
def analyser():
	if len(os.listdir()) > 0:
		list_img_sqrs = video_process()
	return render_template('analysis.html', list_img_sqrs=list_img_sqrs)

if __name__ == "__main__":
    app.run(debug=True)
