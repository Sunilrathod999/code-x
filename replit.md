# MTS Furnitech - Professional Furniture Installation Services

## Overview

MTS Furnitech is a professional furniture installation service website built with Flask. The application provides a comprehensive platform for customers to browse services, contact the business, and for administrators to manage content and services. The website specializes in both office and home furniture installation services.

## System Architecture

The application follows a traditional Flask web application architecture with the following components:

- **Frontend**: HTML templates with Bootstrap 5 CSS framework
- **Backend**: Flask web framework with SQLAlchemy ORM
- **Database**: SQLite (default) with PostgreSQL support via environment variable
- **Authentication**: Session-based admin authentication
- **File Storage**: Local file system for image uploads

## Key Components

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive design
- **Static Assets**: CSS, JavaScript, and uploaded images served from static folder
- **User Interface**: Multi-page application with navigation between home, services, about, and contact pages
- **Admin Interface**: Separate admin dashboard for content management

### Backend Architecture
- **Web Framework**: Flask with SQLAlchemy for database operations
- **Models**: Five main entities (Admin, Content, Service, ContactMessage, SiteSettings)
- **Authentication**: Simple username/password authentication for admin users
- **File Upload**: Secure file handling with size limits and type validation
- **Content Management**: Dynamic content editing for home and about pages

### Database Schema
- **Admin**: User authentication (id, username, password_hash)
- **Content**: Page content management (id, section, content, timestamps)
- **Service**: Service listings (id, title, description, category, image_path, order_index, is_active, created_at)
- **ContactMessage**: Customer inquiries (id, name, phone, service_interest, message, is_read, created_at)
- **SiteSettings**: Global settings (id, logo_path, whatsapp_number, company_name, updated_at)

## Data Flow

1. **Public Pages**: Users browse services, view content, and submit contact forms
2. **Contact System**: Form submissions are stored in database for admin review
3. **Admin Dashboard**: Authenticated admins can manage content, services, and view messages
4. **Content Management**: Dynamic content updates for home and about pages
5. **Service Management**: CRUD operations for service listings with image uploads

## External Dependencies

### Frontend Dependencies
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements
- **CDN-hosted**: Both libraries loaded from CDN for performance

### Backend Dependencies
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Werkzeug**: Security utilities and file handling
- **Flask-Login**: User session management (imported but not fully implemented)

### Database
- **SQLite**: Default database for development
- **PostgreSQL**: Supported via DATABASE_URL environment variable for production

## Deployment Strategy

The application is configured for flexible deployment:

- **Development**: SQLite database with debug mode enabled
- **Production**: Environment variable support for database URL and secret key
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies
- **File Uploads**: Configurable upload directory with size limits
- **Session Management**: Environment-based secret key configuration

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Secret key for session security

### File Structure
- Static files served from `/static/` directory
- Upload folder at `/static/uploads/`
- Templates organized in `/templates/` with admin subdirectory

## Changelog
- July 07, 2025. Initial setup
- July 07, 2025. Added contact information management with phone, email, address fields
- July 07, 2025. Updated About Us and Home page text styling with highlighted keywords
- July 07, 2025. Optimized service image loading with lazy loading and improved CSS
- July 07, 2025. Added admin password change functionality
- July 07, 2025. Fixed footer layout removing Service Hours section
- July 08, 2025. Added client logos section with auto-scrolling animation
- July 08, 2025. Implemented modern typography with Space Grotesk for headings and Inter for body text
- July 08, 2025. Updated color palette to include #FFC107, #F7F7F7, #333333, #34C759, and #007bff

## User Preferences

Preferred communication style: Simple, everyday language.