"""Sample data for tests."""

SAMPLE_EMAIL = {
    "id": "email_123",
    "from": "sender@example.com",
    "to": ["recipient@example.com"],
    "subject": "Test Email",
    "body": "This is a test email message.",
    "timestamp": "2026-02-04T10:00:00Z",
    "unread": True
}

SAMPLE_MARKET_DATA = {
    "symbol": "AAPL",
    "current_price": 150.25,
    "change": 2.50,
    "change_percent": 1.69,
    "volume": 1234567,
    "timestamp": "2026-02-04T15:30:00Z"
}

SAMPLE_DOCUMENT = {
    "file_path": "/path/to/document.pdf",
    "pages": 10,
    "text": "Sample document content...",
    "extracted_at": "2026-02-04T12:00:00Z"
}
