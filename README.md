# 🚗 Ride Management System API Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

## 🚖 Ride Endpoints

### 1️⃣ Create a Ride
- **Endpoint:** `POST /rides/`
- **Description:** Create a new ride request.
- **Request Body:**  
  ```json
  {
    "user_id": 1,
    "pickup_location": "123 Street, City",
    "dropoff_location": "456 Avenue, City",
    "ride_status": "pending"
  }
  ```
- **Response:**  
  ```json
  {
    "id": 10,
    "user_id": 1,
    "pickup_location": "123 Street, City",
    "dropoff_location": "456 Avenue, City",
    "ride_status": "pending"
  }
  ```

### 2️⃣ Get Ride Details
- **Endpoint:** `GET /rides/<ride_id>/`
- **Description:** Retrieve details of a specific ride.
- **Response:**  
  ```json
  {
    "id": 10,
    "user_id": 1,
    "pickup_location": "123 Street, City",
    "dropoff_location": "456 Avenue, City",
    "ride_status": "pending"
  }
  ```

### 3️⃣ Accept a Ride
- **Endpoint:** `POST /rides/<ride_id>/accept_ride/`
- **Description:** Driver accepts a ride.
- **Response:**  
  ```json
  {
    "message": "Ride accepted",
    "ride_status": "accepted"
  }
  ```

### 4️⃣ Match a Driver
- **Endpoint:** `POST /rides/<ride_id>/match_driver/`
- **Description:** Automatically match a ride with an available driver.
- **Response:**  
  ```json
  {
    "message": "Driver matched successfully",
    "driver_id": 5
  }
  ```

### 5️⃣ Update Ride Location
- **Endpoint:** `PUT /rides/<ride_id>/update-location/`
- **Description:** Update the driver's current location.
- **Request Body:**  
  ```json
  {
    "latitude": 37.7749,
    "longitude": -122.4194
  }
  ```
- **Response:**  
  ```json
  {
    "message": "Location updated successfully"
  }
  ```

### 6️⃣ Update Ride Status
- **Endpoint:** `POST /rides/<ride_id>/update_status/`
- **Description:** Change the ride status (e.g., "completed", "canceled").
- **Request Body:**  
  ```json
  {
    "ride_status": "completed"
  }
  ```
- **Response:**  
  ```json
  {
    "message": "Ride status updated",
    "ride_status": "completed"
  }
  ```

### 7️⃣ List All Rides
- **Endpoint:** `GET /rides/`
- **Description:** Retrieve a list of all ride requests.
- **Response:**  
  ```json
  [
    {
      "id": 10,
      "user_id": 1,
      "pickup_location": "123 Street, City",
      "dropoff_location": "456 Avenue, City",
      "ride_status": "pending"
    },
    {
      "id": 11,
      "user_id": 2,
      "pickup_location": "789 Road, City",
      "dropoff_location": "101 Blvd, City",
      "ride_status": "completed"
    }
  ]
  ```

## 🛠 Error Handling
All error responses will have the following format:  
```json
{
  "error": "Invalid ride ID"
}
```