# Doctor Search API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Endpoints

### 1. List All Doctors
**GET** `/api/doctors/`

Returns a paginated list of all doctors.

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10, max: 100)
- `specialization` - Filter by specialization
- `location` - Filter by location
- `search` - Search by name or specialization
- `ordering` - Sort by field (name, experience)

**Example:**
```
GET /api/doctors/?specialization=Cardiology&page_size=5
```

**Response:**
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/doctors/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Dr. John Smith",
            "specialization": "Cardiology",
            "location": "New York",
            "experience": 10,
            "contact": "555-1234"
        },
        ...
    ]
}
```

---

### 2. Get Doctor by ID
**GET** `/api/doctors/{id}/`

Returns detailed information about a specific doctor including appointment count.

**Example:**
```
GET /api/doctors/1/
```

**Response:**
```json
{
    "id": 1,
    "name": "Dr. John Smith",
    "specialization": "Cardiology",
    "location": "New York",
    "experience": 10,
    "contact": "555-1234",
    "appointment_count": 5
}
```

---

### 3. Search Doctors
**GET** `/api/doctors/search/`

Advanced search endpoint with multiple filtering options.

**Query Parameters:**
- `name` - Search by doctor name (case-insensitive partial match)
- `specialization` - Filter by specialization
- `location` - Filter by location
- `min_experience` - Filter by minimum years of experience
- `page` - Page number (default: 1)
- `page_size` - Items per page

**Examples:**

Search by name and location:
```
GET /api/doctors/search/?name=John&location=NYC
```

Filter by minimum experience:
```
GET /api/doctors/search/?min_experience=5&specialization=Cardiology
```

Combined search:
```
GET /api/doctors/search/?name=Smith&location=New%20York&min_experience=5&specialization=Cardiology
```

**Response:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Dr. John Smith",
            "specialization": "Cardiology",
            "location": "New York",
            "experience": 10,
            "contact": "555-1234"
        }
    ]
}
```

---

### 4. Get Doctor's Appointments
**GET** `/api/doctors/{id}/appointments/`

Returns all appointments for a specific doctor.

**Example:**
```
GET /api/doctors/1/appointments/
```

**Response:**
```json
[
    {
        "id": 1,
        "patient_name": "John Doe",
        "doctor": 1,
        "doctor_name": "Dr. John Smith",
        "date": "2024-03-30"
    }
]
```

---

### 5. Create Doctor (Admin)
**POST** `/api/doctors/`

Create a new doctor record.

**Request Body:**
```json
{
    "name": "Dr. Jane Doe",
    "specialization": "Dermatology",
    "location": "Los Angeles",
    "experience": 8,
    "contact": "555-5678"
}
```

**Response:** (201 Created)
```json
{
    "id": 2,
    "name": "Dr. Jane Doe",
    "specialization": "Dermatology",
    "location": "Los Angeles",
    "experience": 8,
    "contact": "555-5678"
}
```

---

### 6. Update Doctor (Admin)
**PUT** `/api/doctors/{id}/`

Update an existing doctor record.

**Request Body:**
```json
{
    "name": "Dr. Jane Doe",
    "specialization": "Dermatology",
    "location": "Los Angeles",
    "experience": 9,
    "contact": "555-5678"
}
```

---

### 7. Partial Update Doctor (Admin)
**PATCH** `/api/doctors/{id}/`

Partially update a doctor record.

**Request Body:**
```json
{
    "experience": 9
}
```

---

### 8. Delete Doctor (Admin)
**DELETE** `/api/doctors/{id}/`

Delete a doctor record.

**Response:** (204 No Content)

---

## Appointments Endpoints

### 1. List All Appointments
**GET** `/api/appointments/`

Returns a paginated list of all appointments.

**Query Parameters:**
- `page` - Page number
- `page_size` - Items per page
- `doctor` - Filter by doctor ID
- `date` - Filter by specific date
- `ordering` - Sort by field (date, patient_name)

**Example:**
```
GET /api/appointments/?doctor=1&ordering=-date
```

---

### 2. Get Appointment by ID
**GET** `/api/appointments/{id}/`

Returns details of a specific appointment.

---

### 3. Create Appointment
**POST** `/api/appointments/`

Create a new appointment.

**Request Body:**
```json
{
    "patient_name": "John Doe",
    "doctor": 1,
    "date": "2024-03-30"
}
```

---

### 4. Update/Delete Appointments
**PUT/PATCH/DELETE** `/api/appointments/{id}/`

Update or delete existing appointments.

---

## Error Responses

**400 Bad Request:**
```json
{
    "error": "min_experience must be an integer"
}
```

**404 Not Found:**
```json
{
    "detail": "Not found."
}
```

**405 Method Not Allowed:**
```json
{
    "detail": "Method 'POST' not allowed."
}
```

---

## Testing with cURL

List all doctors:
```bash
curl http://localhost:8000/api/doctors/
```

Search for doctors:
```bash
curl "http://localhost:8000/api/doctors/search/?name=John&min_experience=5"
```

Get specific doctor:
```bash
curl http://localhost:8000/api/doctors/1/
```

Get doctor's appointments:
```bash
curl http://localhost:8000/api/doctors/1/appointments/
```

Create a new doctor (requires authentication):
```bash
curl -X POST http://localhost:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Dr. Jane","specialization":"Surgery","location":"Boston","experience":5,"contact":"555-9999"}'
```

---

## Filtering, Searching, and Ordering

### Filter
Use specific fields to filter:
```
GET /api/doctors/?specialization=Cardiology&location=New%20York
```

### Search
Search across multiple fields:
```
GET /api/doctors/?search=John
```

### Order/Sort
Sort results ascending or descending:
```
GET /api/doctors/?ordering=name           # Ascending
GET /api/doctors/?ordering=-experience    # Descending
```

---

## Pagination

Default page size is 10 items. Customize pagination:

```
GET /api/doctors/?page=2&page_size=20
```

Response includes pagination metadata:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/doctors/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## API Browser

Django REST Framework provides a browsable API at:
```
http://localhost:8000/api/
```

Visit this URL in your browser to explore the API interactively.
