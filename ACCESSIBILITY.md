
# Accessibility

We want the University Enrollment and Course Registration System to be usable by as many people as possible, including users with different abilities, devices, and levels of technical experience.

Accessibility matters because every student and contributor should be able to navigate the application, understand its information, and complete tasks without unnecessary barriers.

This document explains our accessibility priorities, contributor expectations, known limitations, and how to report accessibility issues.

## Priorities

We aim to make the application simple, readable, and easy to navigate.

Our accessibility priorities include:

- **Readable content:** Use clear labels, readable fonts, and appropriate text sizes.
- **Color and contrast:** Maintain sufficient contrast between text, backgrounds, and interface elements.
- **Keyboard navigation:** Allow users to navigate and interact with the application using a keyboard whenever possible.
- **Consistent layout:** Keep buttons, menus, forms, and navigation elements organized and predictable.
- **Clear feedback:** Display understandable messages for successful actions, errors, and invalid inputs.
- **Simple language:** Use straightforward instructions and labels throughout the application.

These are development goals and do not represent verified accessibility compliance.

## Contributor Expectations

All contributors should consider accessibility when developing or modifying the application.

Contributors are expected to:

- Use descriptive labels for buttons, input fields, and other interface elements.
- Avoid relying on color alone to communicate important information.
- Maintain readable text and consistent layouts.
- Provide clear error messages and input instructions.
- Consider keyboard accessibility when adding interactive components.
- Test interface changes before submitting them.
- Report any accessibility issues discovered during development or testing.

For changes involving the user interface, contributors should include screenshots when useful and describe the changes made.

## Reporting Accessibility Issues

If you encounter an accessibility barrier while using the application, please report it through the repository's GitHub Issues page:

https://github.com/MikeyMadeIt/university_enrollment-system/issues

When reporting an issue, include:

- The feature or page where the problem occurred.
- What you were trying to do.
- What happened and what you expected to happen.
- Your operating system and relevant environment details.
- Screenshots or recordings, if available.

You do not need to disclose any personal or medical information to report an accessibility issue.

### Severity

Accessibility issues may be categorized based on their impact:

- **Critical:** A barrier prevents users from completing an essential task, such as registering a student or enrolling in a course.
- **High:** A major feature is difficult or impossible to use because of an accessibility barrier.
- **Medium:** A feature remains usable, but navigation or understanding is significantly affected.
- **Low:** Minor visual or usability issues that do not prevent users from completing tasks.

The project maintainers may review and assign the appropriate severity.

### How We Respond

Reported issues will be reviewed by the project team.

We will:
- Acknowledge reported issues when possible.
- Review the problem and determine its impact.
- Discuss possible solutions with the contributors.
- Provide updates when progress is made.
- Test proposed fixes before considering an issue resolved.

As this is an academic project maintained by student contributors, response and resolution times may vary.

## Ownership and Maintenance

Accessibility is a shared responsibility among all project contributors.

The project leader and assigned UI developer are primarily responsible for coordinating accessibility improvements, reviewing interface changes, and addressing reported issues.

All contributors are encouraged to identify and report accessibility barriers throughout development and testing.

This document should be reviewed whenever significant changes are made to the application's interface or accessibility practices.

## Supported Environments

The application is designed as a Python desktop application using Tkinter.

Its intended environment includes:

- **Operating Systems:** Windows, Linux, and macOS, subject to Python and Tkinter availability.
- **Interface:** Tkinter graphical user interface.
- **Input Methods:** Keyboard and mouse.
- **Storage:** Local JSON files.

The project has not yet completed formal accessibility testing across different operating systems, screen readers, or assistive technologies. Compatibility should not be assumed until tested.

## Known Limitations

The application is still under development, and some accessibility limitations may remain.

Potential areas requiring further testing include:

- Screen reader compatibility.
- Keyboard navigation across all pages and dialogs.
- Text scaling and display resizing.
- Color contrast across different interface themes.
- Consistent focus indicators for interactive elements.

These areas will be reviewed and improved as development progresses.

## Feedback and Improvements

We welcome suggestions from users and contributors who want to help make the application more accessible.

For general suggestions about this document or accessibility practices, you may open a GitHub Issue in the repository:

https://github.com/MikeyMadeIt/university_enrollment-system/issues

Accessibility improvements are an ongoing part of making the system easier to use, understand, and maintain.
