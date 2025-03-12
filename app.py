from flask import Flask, request, render_template, jsonify
import ssl
import socket

app = Flask(__name__)

def get_san(hostname, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                san = cert.get('subjectAltName', [])
                dns_names = [value for name, value in san if name == "DNS"]
                return dns_names if dns_names else ["No SANs found."]
    except socket.timeout:
        return ["Error: Connection Timed Out"]
    except ssl.SSLError:
        return ["Error: SSL/TLS Certificate Not Found or Invalid"]
    except Exception as e:
        return [f"Error: {str(e)}"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_san', methods=['POST'])
def fetch_san():
    domain = request.form.get('domain')
    if not domain:
        return jsonify({"san": ["Invalid Input: Please enter a domain name"]})
    
    san_list = get_san(domain)
    return jsonify({"san": san_list}) 

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
