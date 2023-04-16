run :
	streamlit run streamlit_timeslicer/app.py

runweb :
	streamlit run streamlit_timeslicer/app_web.py

setup :
	pip install -r requirements.txt
	sudo apt install ffmpeg

setup_mac :
	pip install -r requirements.txt
	brew install ffmpeg