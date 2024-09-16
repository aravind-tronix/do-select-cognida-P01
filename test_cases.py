from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "visit /docs for swagger"}


def test_calc_no_body():
    response = client.post("/api/v1/execute-formula")
    assert response.status_code == 422


def test_calc_valid_body():
    fieldA = [10, 20]
    response = client.post(
        "/api/v1/execute-formula",
        json={
            "data": [{"id": 1, "fieldA": fieldA[0]}, {"id": 2, "fieldA": fieldA[1]}],
            "formulas": [
                {
                    "outputVar": "result",
                    "expression": "fieldA + 10",
                    "inputs": [{"varName": "fieldA", "varType": "number"}],
                }
            ],
        },
    )
    assert response.status_code == 200
    responseResult = response.json()
    assert responseResult["message"]["results"]["result"] == [fieldA[0] + 10, fieldA[1] + 10]


def test_calc_valid_body_nested():
    fieldA = [10, 20]
    response = client.post(
        "/api/v1/execute-formula",
        json={
            "data": [{"id": 1, "fieldA": 10, "fieldB": 2}, {"id": 2, "fieldA": 20, "fieldB": 3}],
            "formulas": [
                {
                    "outputVar": "sumResult",
                    "expression": "fieldA + fieldB",
                    "inputs": [
                        {"varName": "fieldA", "varType": "number"},
                        {"varName": "fieldB", "varType": "number"},
                    ],
                },
                {
                    "outputVar": "finalResult",
                    "expression": "sumResult * 2 + fieldA",
                    "inputs": [
                        {"varName": "sumResult", "varType": "number"},
                        {"varName": "fieldA", "varType": "number"},
                    ],
                },
            ],
        },
    )
    assert response.status_code == 200
    responseResult = response.json()
    assert (
        responseResult["message"]["message"]
        == "The formulas were executed successfully with variable-based chaining."
    )


def test_calc_empty_body():
    response = client.post("/api/v1/execute-formula", json={"data": [{}], "formulas": [{}]})
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Each item in data must be a non-empty dictionary"
    )
    assert (
        response.json()["detail"][1]["msg"]
        == "Value error, Each item in formulas must be a non-empty dictionary"
    )


def test_calc_valid_body_currency():
    fieldA = [10, 20]
    response = client.post(
        "/api/v1/execute-formula",
        json={
            "data": [
                {
                    "id": 1,
                    "product": "Laptop",
                    "unitPrice": "1000 USD",
                    "quantity": 5,
                    "discount": "10%",
                },
                {
                    "id": 2,
                    "product": "Smartphone",
                    "unitPrice": "500 USD",
                    "quantity": 10,
                    "discount": "5%",
                },
                {
                    "id": 3,
                    "product": "Tablet",
                    "unitPrice": "300 USD",
                    "quantity": 15,
                    "discount": "0%",
                },
            ],
            "formulas": [
                {
                    "outputVar": "revenue",
                    "expression": "((unitPrice * quantity) - (unitPrice * quantity * (discount / 100)))",
                    "inputs": [
                        {"varName": "unitPrice", "varType": "currency"},
                        {"varName": "quantity", "varType": "number"},
                        {"varName": "discount", "varType": "percentage"},
                    ],
                }
            ],
        },
    )
    assert response.status_code == 200
    responseResult = response.json()
    assert responseResult["message"]["message"] == "The formulas were executed successfully."


def test_calc_valid_body_datetime():
    fieldA = [10, 20]
    response = client.post(
        "/api/v1/execute-formula",
        json={
            "data": [
                {"id": 1, "eventDate": "2024-09-14 10:30:00", "daysToAdd": 5},
                {"id": 2, "eventDate": "2024-09-14 08:00:00", "daysToAdd": 10},
            ],
            "formulas": [
                {
                    "outputVar": "newDate",
                    "expression": "eventDate + timedelta(days=daysToAdd)",
                    "inputs": [
                        {"varName": "eventDate", "varType": "datetime"},
                        {"varName": "daysToAdd", "varType": "number"},
                    ],
                }
            ],
        },
    )
    assert response.status_code == 200
    responseResult = response.json()
    assert responseResult["message"]["message"] == "The formulas were executed successfully."
