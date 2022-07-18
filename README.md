# boredgames - WIP

Back-end written in Python + FastAPI, Front-end in Svelte + Tailwind

The goal is to create an open-source central hub where lots of board games can be played by anyone around the world

Play connect 4, checkers, battleship, etc... with your friends, or anyone online!

Fully functioning engine (with valid draw, win, lose, movement etc...) with support for private and public lobbies for:
    connect 4
    checkers
    battleship (will be implemented someday)

If you have any suggestions, feedbacks, or anything really, feel free to create an issue or contact me via email :)

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```
To run the python back-end server:

```bash
pip install fastapi

pip install "uvicorn[standard]"

# and run the following command in the back-end folder

uvicorn main:app --reload
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.
