
uvicorn main:app --reload


after i have uploaded the file to my chatbot, i want to process it with my langchain chain to summarize the uploaded doc and then make an entry to a new sqllite db "summaries.db" in the backend and list it in streamlit frotend in the frontend, so that when ever user logs in, he will se the list of documents he summarized earlier.