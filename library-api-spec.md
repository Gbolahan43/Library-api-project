# Library Management API - Project Specification Document

**Project Name:** Library-Api  
**Technology Stack:** FastAPI, Python  
**Date:** January 2026  
**Status:** Initial Specification & Requirements Analysis

---

## 1. Executive Overview

Library-Api is a RESTful backend service designed to manage a comprehensive library system. It enables librarians to efficiently manage book inventory, track book borrowing, manage user accounts, calculate overdue fines, and organize books by sections. The API provides a robust foundation for a complete library management system.

---

## 2. Core Functionalities

### 2.1 Book Management
- **Add Book:** Create new book records with complete metadata
- **Update Book:** Modify book information (title, author, ISBN, etc.)
- **Delete Book:** Remove books from the system
- **Get Book by ID:** Retrieve specific book details using unique identifier
- **Get All Books:** List all books with pagination support
- **Get Books by Section:** Filter books by library section (Sciences, Arts, Social Studies, Economics, Religion, General Studies)
- **Get Available Books:** View only books currently not borrowed

### 2.2 Book Borrowing & Return
- **Borrow Book:** Record when a user borrows a book with due date
- **Return Book:** Mark book as returned, calculate any applicable fines
- **Track Borrowing History:** Maintain records of who borrowed what and when
- **Manage Due Dates:** Set and track borrowing periods (default: 14 days, configurable)

### 2.3 User Management (Librarians)
- **Create User:** Register new librarian accounts
- **Get User Details:** Retrieve librarian information
- **List Users:** View all registered librarians
- **User Identification:** Unique User IDs for tracking borrowing actions

### 2.4 Fine Management
- **Calculate Fines:** Automatic fine calculation for overdue books
- **Fine Tracking:** Record and manage fines per user
- **Fine Payment:** Mark fines as paid
- **View Outstanding Fines:** Check unpaid fines for users

### 2.5 Reporting & Analytics (Future Phase)
- **Borrowing Statistics:** Track most borrowed books
- **Overdue Reports:** List all overdue books
- **User Activity:** Track which librarians have made changes
- **Inventory Reports:** Current book counts and availability

---

## 3. Data Models & Database Schema

### 3.1 Core Entities

#### **Books Table**
```
id (Primary Key) - UUID
title - String (Required)
author - String (Required)
isbn - String (Unique, Required)
publication_year - Integer
publisher - String
section - Enum (Sciences, Arts, Social Studies, Economics, Religion, General Studies)
quantity - Integer (Total copies)
available_quantity - Integer (Copies available for borrowing)
description - Text
created_at - Timestamp
updated_at - Timestamp
is_active - Boolean (Soft delete support)
```

#### **Users (Librarians) Table**
```
id (Primary Key) - UUID
name - String (Required)
email - String (Unique, Required)
phone - String (Optional)
employee_id - String (Unique)
role - String (Librarian, Admin, etc.)
created_at - Timestamp
updated_at - Timestamp
is_active - Boolean
```

#### **Borrowing Records Table**
```
id (Primary Key) - UUID
book_id (Foreign Key) - References Books
user_id (Foreign Key) - References Users
borrowed_at - Timestamp
due_date - Timestamp
returned_at - Timestamp (NULL if not yet returned)
status - Enum (Active, Returned, Overdue)
created_at - Timestamp
```

#### **Fines Table**
```
id (Primary Key) - UUID
borrowing_id (Foreign Key) - References Borrowing Records
user_id (Foreign Key) - References Users
amount - Decimal
fine_date - Timestamp
due_date - Timestamp (When fine must be paid)
status - Enum (Pending, Paid, Waived, Overdue)
paid_at - Timestamp (NULL if unpaid)
notes - Text
created_at - Timestamp
```

#### **Book Sections Table** (Lookup/Reference)
```
id (Primary Key) - Integer
name - String (Unique)
description - Text
created_at - Timestamp
```

### 3.2 Database Relationships
- **Books ↔ Borrowing Records:** One-to-Many (One book can have many borrowing records)
- **Users ↔ Borrowing Records:** One-to-Many (One user can borrow many books)
- **Borrowing Records ↔ Fines:** One-to-Many (One borrowing can generate multiple fine records)
- **Users ↔ Fines:** One-to-Many (One user can have multiple fines)
- **Books ↔ Sections:** Many-to-One (Books belong to one section)

---

## 4. RESTful API Endpoints

### 4.1 Book Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|-----------|
| POST | `/api/v1/books` | Add new book | Request body with book details |
| GET | `/api/v1/books` | Get all books | Query: `section`, `page`, `limit` |
| GET | `/api/v1/books/{book_id}` | Get book by ID | Path: `book_id` |
| GET | `/api/v1/books/section/{section_name}` | Get books by section | Path: `section_name` |
| GET | `/api/v1/books/available` | Get available books | Query: `page`, `limit` |
| PUT | `/api/v1/books/{book_id}` | Update book details | Path: `book_id`, Request body |
| DELETE | `/api/v1/books/{book_id}` | Delete book (soft delete) | Path: `book_id` |
| PATCH | `/api/v1/books/{book_id}/quantity` | Update book quantity | Path: `book_id`, Request body |

### 4.2 Borrowing Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|-----------|
| POST | `/api/v1/borrowing` | Borrow a book | Request body: `book_id`, `user_id` |
| GET | `/api/v1/borrowing/{borrowing_id}` | Get borrowing record | Path: `borrowing_id` |
| GET | `/api/v1/borrowing/user/{user_id}` | Get user's borrowing history | Path: `user_id`, Query: `status` |
| GET | `/api/v1/borrowing/book/{book_id}` | Get borrowing history for book | Path: `book_id` |
| PUT | `/api/v1/borrowing/{borrowing_id}/return` | Return a book | Path: `borrowing_id` |
| GET | `/api/v1/borrowing/overdue` | Get all overdue books | Query: `page`, `limit` |

### 4.3 User (Librarian) Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|-----------|
| POST | `/api/v1/users` | Create new librarian | Request body with user details |
| GET | `/api/v1/users` | Get all users | Query: `page`, `limit` |
| GET | `/api/v1/users/{user_id}` | Get user details | Path: `user_id` |
| PUT | `/api/v1/users/{user_id}` | Update user information | Path: `user_id`, Request body |
| DELETE | `/api/v1/users/{user_id}` | Delete user | Path: `user_id` |

### 4.4 Fine Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|-----------|
| GET | `/api/v1/fines` | Get all fines | Query: `user_id`, `status`, `page`, `limit` |
| GET | `/api/v1/fines/{fine_id}` | Get fine details | Path: `fine_id` |
| GET | `/api/v1/fines/user/{user_id}` | Get fines for user | Path: `user_id`, Query: `status` |
| PUT | `/api/v1/fines/{fine_id}/pay` | Mark fine as paid | Path: `fine_id`, Request body with payment info |
| GET | `/api/v1/fines/outstanding` | Get outstanding fines | Query: `page`, `limit` |

### 4.5 Section Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|-----------|
| GET | `/api/v1/sections` | Get all sections | - |
| GET | `/api/v1/sections/{section_id}` | Get section details | Path: `section_id` |
| POST | `/api/v1/sections` | Create new section | Request body with section details |

---

## 5. Fine Calculation Logic

### 5.1 Fine Rules
- **Base Fine Rate:** 50 currency units per day (configurable)
- **Grace Period:** None (fines apply immediately on due date)
- **Maximum Daily Fine:** No limit (or configurable cap)
- **Fine Accrual:** Calculated daily for active overdue books

### 5.2 Fine Calculation Formula
```
Daily Fine = (Current Date - Due Date) × Base Rate per Day

Example:
- Book due: January 10, 2026
- Book returned: January 20, 2026 (10 days late)
- Fine Amount = 10 days × 50 currency units = 500 currency units
```

### 5.3 Fine Management Scenarios
1. **On Time Return:** No fine, status: "Completed"
2. **Late Return:** Fine automatically generated, status: "Overdue"
3. **Fine Payment:** Mark as "Paid" with payment date
4. **Fine Waiver:** Admin can mark as "Waived" with notes

---

## 6. Request/Response Schema Examples

### 6.1 Add Book Request
```json
{
  "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
  "author": "Robert C. Martin",
  "isbn": "978-0132350884",
  "publication_year": 2008,
  "publisher": "Prentice Hall",
  "section": "Sciences",
  "quantity": 5,
  "description": "A guide to writing clean, maintainable code"
}
```

### 6.2 Add Book Response
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
  "author": "Robert C. Martin",
  "isbn": "978-0132350884",
  "publication_year": 2008,
  "publisher": "Prentice Hall",
  "section": "Sciences",
  "quantity": 5,
  "available_quantity": 5,
  "description": "A guide to writing clean, maintainable code",
  "created_at": "2026-01-13T14:30:00Z",
  "updated_at": "2026-01-13T14:30:00Z",
  "is_active": true
}
```

### 6.3 Borrow Book Request
```json
{
  "book_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660f9500-f40c-52e5-b827-557766551111",
  "borrowing_period_days": 14
}
```

### 6.4 Borrow Book Response
```json
{
  "id": "770g0611-g51d-63f6-c938-668877662222",
  "book_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660f9500-f40c-52e5-b827-557766551111",
  "book_title": "Clean Code: A Handbook of Agile Software Craftsmanship",
  "borrowed_at": "2026-01-13T14:30:00Z",
  "due_date": "2026-01-27T14:30:00Z",
  "returned_at": null,
  "status": "Active",
  "created_at": "2026-01-13T14:30:00Z"
}
```

### 6.5 Return Book Request
```json
{
  "borrowing_id": "770g0611-g51d-63f6-c938-668877662222"
}
```

### 6.6 Return Book Response
```json
{
  "id": "770g0611-g51d-63f6-c938-668877662222",
  "book_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660f9500-f40c-52e5-b827-557766551111",
  "borrowed_at": "2026-01-13T14:30:00Z",
  "due_date": "2026-01-27T14:30:00Z",
  "returned_at": "2026-02-05T10:15:00Z",
  "status": "Returned",
  "days_overdue": 9,
  "fine_generated": {
    "id": "880h1722-h62e-74g7-d049-779988773333",
    "amount": 450,
    "status": "Pending"
  }
}
```

---

## 7. Key Features & Suggested Enhancements

### 7.1 Implemented Features
✅ Complete CRUD operations for books  
✅ Borrowing and return tracking  
✅ Automatic fine calculation  
✅ Book section organization  
✅ User management (librarians)  
✅ Comprehensive borrowing history  

### 7.2 Recommended Features
- **Search & Filtering:** Advanced search by title, author, ISBN, publication year
- **Pagination:** Efficient data retrieval for large datasets
- **Data Validation:** Comprehensive input validation with Pydantic
- **Error Handling:** Standard HTTP status codes with meaningful error messages
- **Logging:** Activity logging for audit trails
- **Authentication & Authorization:** JWT tokens for secure access (Bearer tokens)
- **Rate Limiting:** Prevent API abuse
- **CORS Configuration:** Handle cross-origin requests if needed
- **Soft Deletes:** Preserve data integrity with logical deletes
- **Audit Trail:** Track who created/modified records with timestamps
- **Email Notifications:** Remind users of due dates and overdue books (Future)
- **Reservation System:** Allow users to reserve borrowed books (Future)
- **Book Ratings & Reviews:** Community engagement feature (Future)

### 7.3 Data Validation Rules
```
Books:
  - Title: Required, 1-255 characters
  - Author: Required, 1-255 characters
  - ISBN: Required, unique, format: XXX-X-XXXXX-X or 13 digits
  - Publication Year: 1800-current year
  - Quantity: Positive integer, minimum 1
  - Available Quantity: 0 to Quantity (system calculated)

Users:
  - Name: Required, 2-255 characters
  - Email: Required, unique, valid email format
  - Phone: Optional, valid format
  - Employee ID: Unique

Borrowing:
  - Due Date: Must be future date
  - Borrowing Period: Default 14 days, configurable 1-90 days
  - Book must be available (available_quantity > 0)

Fines:
  - Amount: Positive decimal
  - Auto-calculated based on days overdue
```

---

## 8. Configuration Requirements

### 8.1 Environment Variables
```
DATABASE_URL=postgresql://user:password@localhost:5432/library_db
SQLALCHEMY_TRACK_MODIFICATIONS=False
JWT_SECRET_KEY=your-secret-key-here
FINE_RATE_PER_DAY=50
DEFAULT_BORROWING_PERIOD=14
API_VERSION=v1
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 8.2 Database Configuration
- **Database Type:** PostgreSQL (recommended) or SQLite (for development)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic for schema management

### 8.3 Dependencies (To be installed)
```
fastapi==0.109.0
uvicorn==0.27.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
psycopg2-binary==2.9.9
alembic==1.13.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

---

## 9. Dummy Data Seeding

The system will include initial database seeding with:

**Sample Books (10+ per section):**
- Sciences: 15 books (programming, physics, chemistry, biology)
- Arts: 10 books (literature, painting, music, design)
- Social Studies: 12 books (history, geography, sociology, psychology)
- Economics: 8 books (macroeconomics, microeconomics, finance)
- Religion: 7 books (comparative religion, theology, philosophy)
- General Studies: 10 books (general knowledge, self-help, autobiography)

**Sample Users (Librarians): 5-10 librarian accounts**

**Sample Borrowing Records: 10-20 active and completed borrowing records**

---

## 10. Error Handling & HTTP Status Codes

| Status | Code | Scenario |
|--------|------|----------|
| 200 | OK | Successful GET, PUT operations |
| 201 | Created | Successful POST (create resource) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input data, validation errors |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate ISBN, email, etc. |
| 422 | Unprocessable Entity | Request validation failed |
| 500 | Server Error | Unexpected server error |

---

## 11. API Response Standard

All API responses will follow a consistent format:

### 11.1 Success Response (Standard)
```json
{
  "success": true,
  "status_code": 200,
  "message": "Operation completed successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Clean Code",
    ...
  }
}
```

### 11.2 List Response (Pagination)
```json
{
  "success": true,
  "status_code": 200,
  "message": "Books retrieved successfully",
  "data": [
    { "id": "...", "title": "...", ... },
    { "id": "...", "title": "...", ... }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 150,
    "total_pages": 15,
    "has_next": true,
    "has_previous": false
  }
}
```

### 11.3 Error Response
```json
{
  "success": false,
  "status_code": 400,
  "message": "Validation error",
  "errors": [
    {
      "field": "isbn",
      "message": "ISBN format is invalid"
    },
    {
      "field": "quantity",
      "message": "Quantity must be a positive integer"
    }
  ]
}
```

---

## 12. Development Roadmap

### **Phase 1: MVP (Current)**
- Core CRUD operations for books
- Basic borrowing and return tracking
- User management
- Fine calculation and tracking
- Basic API endpoints with validation

### **Phase 2: Enhancement**
- Authentication and authorization (JWT)
- Advanced search and filtering
- Pagination implementation
- Logging and audit trails
- Comprehensive error handling
- API documentation (Swagger/OpenAPI)

### **Phase 3: Advanced Features**
- Email notifications
- Book reservation system
- Reporting dashboards
- Analytics and statistics
- Admin panel integration

### **Phase 4: Production Readiness**
- Caching layer (Redis)
- Performance optimization
- Load testing and scaling
- Deployment automation
- Monitoring and alerting

---

## 13. Testing Strategy

### 13.1 Unit Tests
- Model validation tests
- Business logic tests (fine calculation)
- Utility function tests

### 13.2 Integration Tests
- Endpoint testing for all CRUD operations
- Database transaction tests
- Error handling tests

### 13.3 Test Coverage Target
- Minimum 80% code coverage
- All critical paths tested
- Edge case handling validated

---

## 14. Security Considerations

1. **Input Validation:** All inputs validated using Pydantic
2. **SQL Injection Prevention:** Using ORM (SQLAlchemy)
3. **CORS Configuration:** Restrict cross-origin requests appropriately
4. **Rate Limiting:** Implement to prevent API abuse
5. **Authentication:** JWT tokens for user identification
6. **Authorization:** Role-based access control (RBAC)
7. **Data Encryption:** Sensitive data encrypted at rest and in transit
8. **Audit Logging:** Track all data modifications
9. **Environment Variables:** Sensitive configuration stored securely

---

## 15. Deployment Architecture (High-level)

```
Client (Web/Mobile)
    ↓
API Gateway / Load Balancer
    ↓
FastAPI Application (Multiple Instances)
    ↓
PostgreSQL Database
    ↓
Redis Cache (Optional)
```

---

## 16. Success Metrics & KPIs

- **API Response Time:** < 200ms for standard queries
- **Availability:** 99.5% uptime
- **Error Rate:** < 0.1% of requests
- **Data Accuracy:** 100% (no data corruption)
- **Code Quality:** 80%+ test coverage
- **Documentation:** Complete API documentation with examples

---

## 17. Next Steps

1. ✅ **Requirements Approval:** Confirm this specification with stakeholders
2. 📐 **Architecture Design:** Create detailed system architecture diagram
3. 🏗️ **Database Design:** Finalize schema and create ER diagrams
4. 🛠️ **Development Setup:** Initialize project structure and dependencies
5. 📝 **API Implementation:** Build endpoints following this specification
6. 🧪 **Testing:** Comprehensive unit and integration tests
7. 📚 **Documentation:** Full API documentation with examples
8. 🚀 **Deployment:** Set up development and production environments

---

## 18. Appendix: Assumptions & Constraints

### Assumptions
- One library system (single database)
- Librarians manage system directly (no public borrowing)
- Books are physical items (not digital)
- No subscription-based borrowing
- Fine calculation is automatic

### Constraints
- Book can only be borrowed by one user at a time
- Can't modify borrowed book details
- Fine must be paid before borrowing again
- User can borrow multiple books
- System operates within single timezone initially

---

## Document Control

**Version:** 1.0  
**Last Updated:** January 13, 2026  
**Prepared by:** Development Team  
**Status:** Ready for Architecture Phase  

---
