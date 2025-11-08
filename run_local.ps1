# Run Streamlit on all interfaces (0.0.0.0) so mobile devices on the same network can access it
$python = "C:/Users/heman/AppData/Local/Programs/Python/Python311/python.exe"
$script = "app.py"
$port = 8501
& $python -m streamlit run $script --server.address 0.0.0.0 --server.port $port
