run :
	streamlit run streamlit_timeslicer/app.py

runweb :
	streamlit run streamlit_timeslicer/app_web.py

setup :
	pip install -r requirements.txt
	sudo apt install ffmpeg