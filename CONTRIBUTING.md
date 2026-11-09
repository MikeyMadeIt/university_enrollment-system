
# Contributing Guidelines

Thank you for contributing to the University Enrollment and Course Registration System!

To keep our project organized and avoid conflicts, please follow these guidelines when working on the repository.

## 1. Branch Assignment

Each programmer has their own development branch:

| Member | Branch |
|---|---|
| Felix | `dev/felix` |
| Mikey | `dev/mikey` |
| Lopez | `dev/lopez` |

Always work on your assigned branch. Do not commit or push directly to `main`.

## 2. Getting Started

Clone the repository:

```bash
git clone https://github.com/MikeyMadeIt/university_enrollment-system.git
```

Navigate to the project folder:

```bash
cd university_enrollment-system
```

Check out your assigned branch:

```bash
git checkout dev/your-name
```

Replace `your-name` with your assigned branch name.

## 3. Before Starting Work

Always sync your branch with the latest changes from `main`:

```bash
git fetch origin
git merge origin/main
```

This helps keep your branch updated with the latest project files.

## 4. Saving and Pushing Changes

After making changes, check the modified files:

```bash
git status
```

Stage your changes:

```bash
git add .
```

Commit your changes with a clear message:

```bash
git commit -m "feat: add student registration"
```

Push to your assigned branch:

```bash
git push origin dev/your-name
```

## 5. Commit Message Guidelines

Use clear and consistent commit messages.

| Prefix | Usage |
|---|---|
| `feat:` | Adding a new feature |
| `fix:` | Fixing bugs or errors |
| `docs:` | Updating documentation |
| `refactor:` | Improving or restructuring code |
| `test:` | Adding or updating tests |
| `style:` | Formatting or UI changes |

Examples:

```text
feat: add course management
fix: prevent duplicate enrollment
docs: update project structure
test: add enrollment test cases
```

## 6. Important Rules

- Work only on your assigned branch.
- Do not push directly to `main`.
- Do not modify another member's assigned modules without coordination.
- Follow the existing folder structure.
- Use consistent function names and data formats.
- Test your changes before pushing.
- Avoid committing unnecessary files, temporary files, or personal settings.
- Communicate with the team before making major structural changes.

## 7. Branch Synchronization

Whenever new changes are merged into `main`, GitHub Actions will automatically sync the latest changes into:

- `dev/felix`
- `dev/mikey`
- `dev/lopez`

If a merge conflict occurs, coordinate with the team and resolve it before continuing.

## 8. Pull Requests

When your work is ready for integration:

1. Push your changes to your assigned branch.
2. Create a Pull Request targeting `main`.
3. Describe the changes you made.
4. Wait for review and approval before merging.

Only tested and working changes should be merged into `main`.

---

**Reminder:** Keep your code organized, communicate with your teammates, and make sure your contributions work with the rest of the system. Every module is part of one application, so coordination matters.
