# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

Please report (suspected) security vulnerabilities to the repository maintainers via GitHub Security Advisories or by opening an issue. You will receive a response from us within 48 hours. If the issue is confirmed, we will release a patch as soon as possible depending on complexity.

## Security Considerations

When using this project:

1. **Environment Variables**: Never commit actual Telegram bot tokens or chat IDs to the repository
2. **GitHub Secrets**: Use GitHub Secrets for sensitive configuration
3. **Dependencies**: Keep Python dependencies updated by regularly updating `requirements.txt`
4. **Access Control**: Ensure your Telegram bot has appropriate permissions and is only added to intended channels

## Best Practices

- Use the provided `.env.example` file as a template for local development
- Regularly update dependencies to get security patches
- Review any third-party contributions carefully
- Follow the principle of least privilege for bot permissions
