-- Migration: Add authentication and notification support
-- This migration adds password column to Users table and creates Notifications table

-- Add password_hash column to Users table (if not exists)
ALTER TABLE Users ADD COLUMN password_hash TEXT;

-- Create Notifications table
CREATE TABLE IF NOT EXISTS Notifications (
    notification_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_type TEXT NOT NULL CHECK (length(trim(event_type)) > 0),
    request_id INTEGER,
    created_at TEXT NOT NULL,
    read_at TEXT,
    FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (request_id) REFERENCES Requests (request_id) ON DELETE CASCADE
);

-- Create index for faster notification queries
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON Notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON Notifications(created_at);
CREATE INDEX IF NOT EXISTS idx_notifications_read_at ON Notifications(read_at);
