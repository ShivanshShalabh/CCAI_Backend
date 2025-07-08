from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Sample data
mock_data = {
    "ACC1001": {
        "firstName": "John",
        "lastName": "Doe",
        "mobileNumber": "555-1234",
        "emailID": "john.doe@example.com",
        "zipCode": "10001",
        "DOB": "1985-04-12",
        "bills": {
            "2025-04": {
                "amount": 120.50,
                "unitsUsed": 350,
                "dueDate": "2025-04-15",
                "payDate": "2025-04-14",
                "amountReceived": 120.50,
                "lateFees": 0.00
            },
            "2025-05": {
                "amount": 135.75,
                "unitsUsed": 390,
                "dueDate": "2025-05-15",
                "payDate": "2025-05-16",
                "amountReceived": 135.75,
                "lateFees": 5.00
            },
            "2025-06": {
                "amount": 110.00,
                "unitsUsed": 320,
                "dueDate": "2025-06-15",
                "payDate": None,
                "amountReceived": 0.00,
                "lateFees": 10.00
            }
        },
        "outstandingBalance": 120.00
    },
    "ACC1002": {  
        "firstName": "Jane",
        "lastName": "Smith",
        "mobileNumber": "555-5678",
        "emailID": "jane.smith@example.com",
        "zipCode": "10002",
        "DOB": "1990-09-23",
        "bills": {
            "2025-04": {
                "amount": 89.99,
                "unitsUsed": 270,
                "dueDate": "2025-04-10",
                "payDate": "2025-04-09",
                "amountReceived": 89.99,
                "lateFees": 0.00
            },
            "2025-05": {
                "amount": 95.50,
                "unitsUsed": 280,
                "dueDate": "2025-05-10",
                "payDate": "2025-05-10",
                "amountReceived": 95.50,
                "lateFees": 0.00
            },
            "2025-06": {
                "amount": 102.30,
                "unitsUsed": 300,
                "dueDate": "2025-06-10",
                "payDate": "2025-06-12",
                "amountReceived": 102.30,
                "lateFees": 3.00
            }
        },
        "outstandingBalance": 0.00
    },
    "ACC1003": {          
        "firstName": "Robert",
        "lastName": "Brown",
        "mobileNumber": "555-8765",
        "emailID": "robert.brown@example.com",
        "zipCode": "10003",
        "DOB": "1978-12-05",
        "bills": {
            "2025-04": {
                "amount": 200.00,
                "unitsUsed": 600,
                "dueDate": "2025-04-20",
                "payDate": "2025-04-21",
                "amountReceived": 200.00,
                "lateFees": 7.00
            },
            "2025-05": {
                "amount": 210.45,
                "unitsUsed": 620,
                "dueDate": "2025-05-20",
                "payDate": None,
                "amountReceived": 0.00,
                "lateFees": 15.00
            },
            "2025-06": {
                "amount": 198.75,
                "unitsUsed": 590,
                "dueDate": "2025-06-20",
                "payDate": None,
                "amountReceived": 0.00,
                "lateFees": 20.00
            }
        },
        "outstandingBalance": 444.20
    },
    "ACC1004": {   
        "firstName": "Emily",
        "lastName": "Davis",
        "mobileNumber": "555-4321",
        "emailID": "emily.davis@example.com",
        "zipCode": "10004",
        "DOB": "2000-07-19",
        "bills": {
            "2025-04": {
                "amount": 75.25,
                "unitsUsed": 220,
                "dueDate": "2025-04-05",
                "payDate": "2025-04-04",
                "amountReceived": 75.25,
                "lateFees": 0.00
            },
            "2025-05": {
                "amount": 80.00,
                "unitsUsed": 230,
                "dueDate": "2025-05-05",
                "payDate": "2025-05-06",
                "amountReceived": 80.00,
                "lateFees": 2.00
            },
            "2025-06": {
                "amount": 78.90,
                "unitsUsed": 225,
                "dueDate": "2025-06-05",
                "payDate": "2025-06-05",
                "amountReceived": 78.90,
                "lateFees": 0.00
            }
        },
        "outstandingBalance": 0.00
    },
    "ACC1005": {
        "firstName": "Michael",
        "lastName": "Wilson",
        "mobileNumber": "555-6789",
        "emailID": "michael.wilson@example.com",
        "zipCode": "10005",

        "DOB": "1995-03-30",
        "bills": {
            "2025-04": {
                "amount": 150.00,
                "unitsUsed": 450,
                "dueDate": "2025-04-18",
                "payDate": "2025-04-18",
                "amountReceived": 150.00,
                "lateFees": 0.00
            },
            "2025-05": {
                "amount": 145.60,
                "unitsUsed": 440,
                "dueDate": "2025-05-18",
                "payDate": "2025-05-20",
                "amountReceived": 145.60,
                "lateFees": 4.00
            },
            "2025-06": {
                "amount": 155.20,
                "unitsUsed": 460,
                "dueDate": "2025-06-18",
                "payDate": None,
                "amountReceived": 0.00,
                "lateFees": 12.00
            }
        },
        "outstandingBalance": 167.20
    }
}


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message":"Hello World"}), 200


@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    account_id = data.get('accountID')
    dob = data.get('accountHolderDOB')

    if not account_id or not dob:
         return jsonify({"error": "Missing accountID or accountHolderDOB"}), 400

    account = mock_data.get(account_id)
    if account and account['DOB'] == dob:
                return jsonify({k: v for k, v in account.items() if k != 'bills'}), 200
    else:
        return jsonify({"error": "Authentication failed"}), 401

@app.route('/bills', methods=['POST'])
def bills():
    data = request.get_json()
    account_id = data.get('accountID')
    dob = data.get('accountHolderDOB')

    if not account_id or not dob:
         return jsonify({"error": "Missing accountID or accountHolderDOB"}), 400

    account = mock_data.get(account_id)
    if account and account['DOB'] == dob:
                return jsonify({k : json.dumps(v) for k,v in account["bills"].items()}), 200
    else:
        return jsonify({"error": "Authentication failed"}), 401


if __name__ == '__main__': 
    app.run()
