# Notes-Repo

## Description

Notes-Repo is a place where you can make notes (referred to as **Notes** in-code) about whatever topics interest you, and manage them in an easy and convenient way. You can set bookmarks for quick access to the Notes you find most important. You can make folders to organize your Notes according to topic. Notes can also be searched for and saved in an .md file for offline viewing.

### Tools used:

- Flask
- SQLAlchemy
- python-dotenv
- flask_sqlalchemy
- gunicorn
- PyMySQL
- requests

## Usage

<a href=“https://notes-repo.herokuapp.com/” target=“_blank”>Currently deployed version in Heroku</a>

## Support

Send me a GitHub PM for any questions/concerns.

## Roadmap / TO DO

- [ ] Color themes (dark, light, etc.)
- [ ] Feature to download entire folders
- [ ] Add docstrings
- [ ] Flask login implementation for user accounts
- [ ] Publish Note to Reddit (via PRAW)

## Contributing

If you want to contribute, fork this project and open a pull request to the 'develop' branch. Report any issues in the ‘issues’ tab. Please label and report any issues/commits clearly for better cooperation. Good documentation is essential. I'm always open to suggestions on how I can make this website better.

**Important:** For local config / env vars, you need an .env file in the root directory with the following MySQL variables:

```
db_url={}
SECRET_KEY={}
debug={}
env={}
```

## License

<a href=“https://github.com/misterrager8/Notes-Repo/blob/develop/LICENSE.md” target=“_blank”>MIT License</a>

## Project Status

*In development*