# Contributing

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/your-username/pages-telegram-blog.git
cd pages-telegram-blog
pip install -e ".[dev]"
pre-commit install
```

## Making Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test locally (`python scripts/build_index.py`)
5. Commit (pre-commit hooks run automatically)
6. Push and open a Pull Request

## Code Quality

Pre-commit hooks automatically handle:

- **Python**: Ruff formatting/linting, MyPy type checking
- **Web**: Prettier formatting for HTML/CSS/JS
- **Docs**: Markdownlint for documentation
- **Blog**: Post validation and site building

Run manually: `pre-commit run --all-files`

## Adding Posts

1. Create `posts/your-slug/` directory
2. Add `index.html`, `meta.json`, and cover image
3. Test with `python scripts/build_index.py`

## Questions?

Open an issue for any questions!
