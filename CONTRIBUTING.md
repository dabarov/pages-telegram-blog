# Contributing to pages-telegram-blog

Thank you for your interest in contributing! This project welcomes contributions from the community.

## How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs or suggest features
- Please provide detailed information about the issue
- Include steps to reproduce for bugs

### Pull Requests
1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes locally
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Testing
- Test your changes locally before submitting
- Ensure the build scripts work correctly
- Verify Telegram posting works (if applicable)

### Adding New Posts
1. Create a new directory under `posts/` with a descriptive slug
2. Add `index.html` with your blog post content
3. Add `meta.json` with required metadata
4. Add a cover image (PNG/JPG)
5. Test locally by running `python scripts/build_index.py`

## Development Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your Telegram credentials (if testing Telegram features)
3. Install dependencies: `pip install -r requirements.txt`
4. Run build script: `python scripts/build_index.py`

## Questions?

Feel free to open an issue for any questions about contributing!
