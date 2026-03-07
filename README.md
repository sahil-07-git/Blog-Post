# BloggersHub

A clean, full-featured blogging platform built with Django. Write, publish, and engage with readers — no ads, no algorithm, just your words.

---

## Features

- **Authentication** — Sign up, log in, log out with full form validation
- **Post management** — Create, edit, delete, and publish posts with draft/published workflow
- **Reactions** — Like or dislike posts (toggle freely, logged-in users only)
- **Comments & replies** — Threaded one-level reply system on every post
- **Search & filter** — Search by title/content, filter by author, sort by newest/oldest/most liked
- **User profiles** — Public profile pages with bio, join date, post count, likes received, and comments made
- **Landing page** — Homepage with hero, features, how-it-works, and live latest posts
- **Modern UI** — Editorial design system using Lora + DM Sans with warm paper tones

---

## Tech Stack

- **Backend** — Python 3, Django
- **Database** — SQLite (dev), easily swappable to PostgreSQL for production
- **Frontend** — Vanilla HTML/CSS (no JS frameworks)
- **Fonts** — Google Fonts (Lora, DM Sans)

---

## Project Structure

```
bloggershub/
├── blog/                        # Main app
│   ├── migrations/
│   ├── templates/blog/
│   │   ├── home.html
│   │   ├── post_list.html
│   │   ├── post_detail.html
│   │   ├── create_post.html
│   │   ├── edit_post.html
│   │   ├── delete_post.html
│   │   ├── user_profile.html
│   │   └── edit_profile.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
├── accounts/                    # Auth app
│   ├── templates/accounts/
│   │   └── dashboard.html
│   ├── forms.py
│   ├── urls.py
│   └── views.py
├── templates/                   # Global templates
│   ├── layout.html
│   └── registration/
│       ├── login.html
│       └── signup.html
├── static/
│   └── css/
│       └── style.css
├── bloggershub/                 # Project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── requirements.txt
└── .env
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/bloggershub.git
cd bloggershub
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the app.

---

## URL Reference

| URL | View | Description |
|-----|------|-------------|
| `/` | `home` | Landing page |
| `/posts/` | `post_list` | All published posts with search & filter |
| `/post/<id>/` | `post_detail` | Single post with reactions and comments |
| `/create-post/` | `create_post` | Create a new post |
| `/edit-post/<id>/` | `edit_post` | Edit an existing post |
| `/delete-post/<id>/` | `delete_post` | Delete a post |
| `/publish/<id>/` | `publish_post` | Publish a draft |
| `/post/<id>/comment/` | `add_comment` | Submit a comment |
| `/post/<id>/comment/<id>/reply/` | `add_reply` | Reply to a comment |
| `/post/<id>/react/<type>/` | `react_to_post` | Like or dislike a post |
| `/profile/<username>/` | `user_profile` | Public user profile |
| `/profile/edit/` | `edit_profile` | Edit your own profile |
| `/signup/` | `signup_view` | Register a new account |
| `/login/` | `login_view` | Log in |
| `/logout/` | `logout_view` | Log out |
| `/dashboard/` | `dashboard` | Your posts dashboard |
| `/admin/` | Django admin | Admin panel |

---

## Models

### `Post`
| Field | Type | Notes |
|-------|------|-------|
| `title` | CharField | Max 200 chars |
| `content` | TextField | |
| `status` | CharField | `draft` or `published` |
| `author` | ForeignKey | → User |
| `created_at` | DateTimeField | Auto |
| `updated_at` | DateTimeField | Auto |

### `Reaction`
| Field | Type | Notes |
|-------|------|-------|
| `user` | ForeignKey | → User |
| `post` | ForeignKey | → Post |
| `reaction` | CharField | `like` or `dislike` |

One reaction per user per post (`unique_together`). Clicking same reaction again removes it; clicking the other switches it.

### `Comment`
| Field | Type | Notes |
|-------|------|-------|
| `post` | ForeignKey | → Post |
| `author` | ForeignKey | → User |
| `body` | TextField | |
| `parent` | ForeignKey (self) | `null` for top-level, set for replies |
| `created_at` | DateTimeField | Auto |

### `UserProfile`
| Field | Type | Notes |
|-------|------|-------|
| `user` | OneToOneField | → User |
| `bio` | TextField | Optional |

Auto-created via Django signals when a new user registers.

---

## Security

- All write operations (create, edit, delete, comment, react) require login via `@login_required`
- Edit and delete views enforce `author=request.user` ownership — users cannot modify others' content
- Draft posts are hidden from non-authors (`Http404` if accessed directly)
- `SECRET_KEY` and `DEBUG` loaded from environment variables, never hardcoded
- `ALLOWED_HOSTS` configured via `.env`
- CSRF protection on all forms
- Security headers enabled: `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS: DENY`, XSS filter

---

## Requirements

```
django
python-dotenv
```

Install with:

```bash
pip install django python-dotenv
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## License

MIT License. See `LICENSE` for details.
