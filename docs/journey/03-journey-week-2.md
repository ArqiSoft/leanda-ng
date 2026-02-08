# Week 2: Are we really 92% done as the AI reported?

*So from Week 1, Cursor is sure we're almost done. Yay! (???)*

## Started running tests

### Unit tests are failing

Not only the unit tests are failing, most of the services aren't even compiling.

Asked Cursor to address. As it goes though the code, a lot of the 3rd party libraries have drastically changed over 10 years. Big surprise.

The first order of business - make everything compile. Then start researching the missing or incompatible functionality.

### Integration tests are lacking dramatically

Did we miss them during the initial analysis?

Re-analyzing the legacy code and adding the integration tests.

After asking Cursor to do a super-detailed unit, service-level integration and system-integration tests, we found that almost all previously reported progress with tests - was bogus!

## Side quest - Claude Code

So after reading all of the excited reviews, and watching YouTubes, about Claude Code I decided to give it a try. Started with the Pro subscription.

What I asked it to do is the same as Cursor - analyze the current system, propose a comprehensive unit, service-level and system-level integration tests.

And I promptly (pun intended) ran into the token limit, after just 45 min of work. It couldn't complete the analysis of the code base. Hmmm... Switch to $100/mo or just get better at giving directions to Cursor?

## Observations

Most of the models are totally ok to report success when services aren't even compiling.

When asked to run and fix unit tests (should be the most straightforward simplest task right?), Cursor would fix part the problems, report success and say that the rest of the compilation problem were "pre-existing". The pre-existing problem thing is annoyingly persistent in multiple workflows, and it's not obvious how to steer the LLM away from being lazy.

Interesting thing - Cursor would remove functionality in order for a docker build to succeed. I guess - report the successful result on the immediate task at all cost?
