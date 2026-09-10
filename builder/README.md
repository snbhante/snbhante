# [snbhante.github.io](https://github.com/snbhante/snbhante.github.io)

Early Buddhist texts from the Tipitaka (tripitaka). Suttas (sutras) with the Buddha's teachings on mindfulness, insight, wisdom and meditation.

This is a Progressive Web Application which will work in offline, has a splash screen add to home screen etc.
    
## Build, Run & Deploy

### Building and Running on localhost

First clone project:

```sh
git clone https://github.com/snbhante/snbhante.git
```

Make sure project directory

```sh
cd snbhante/builder
```

install dependencies:

```sh
npm install
```

To create a production build:

```sh
npm run build
```

To run build project:

Open the file `dist/index.html` in your browser.

## Running

To run project in Vite with HMR on development or preview mode:

```sh
npm run dev
// or
npm run preview
```

## Deploy

Run theses commands to push and deploy on Github:

```sh
npm run dist
cd ../
git add .
git commit -m "YOUR COMMIT MESSAGE"
git push
```

Project is automatically Hosted on Github Pages. To see [Click here](https://snbhante.github.io/)


That command builds the app and copies `dist` into a separate GitHub Pages repository. On Windows, use PowerShell commands because `cp` and `rm` are Unix commands.

1. Clone your Pages repository once:

```sh
cd $HOME
git clone https://github.com/snbhante/snbhante.github.io.git
```

2. Build and publish:

```sh
cd C:\Users\snbhante\VSCodeProjects\snbhante\builder
npm run build

Copy-Item -Path .\dist\* -Destination "$HOME\snbhante.github.io" -Recurse -Force

cd "$HOME\snbhante.github.io"
git add .
git commit -m "Deploy website"
git push origin main
```

Your site should then be available at:

[https://snbhante.github.io/](https://snbhante.github.io/)

The existing `dist` script fails because `cp`, `rm`, and `~/snbhante.github.io` are Unix-style assumptions. You do not need to run `npm run clean`; keeping `dist` locally is harmless. Ensure GitHub Pages is configured to deploy from the main branch root of `snbhante.github.io`.

<br>

## Credits

Made with [SarbaNanda Bhikkhu](https://github.com/snbhante/)

**☕ Connect with me!**

[![Youtube Badge](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com/channel/UC3WIwB7nbYMEvWW4CGQGYsA)
[![Mail Badge](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:sarbanandabhikkhu@gmail.com)

**This project code with**

<a href=""><img height="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg"></a>
<a href=""><img height="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg"></a>
<a href=""><img height="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sass/sass-original.svg"></a>
<a href=""><img height="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg"></a>

## 📈 Stats

[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![issues](https://img.shields.io/github/issues/snbhante/snbhante.github.io)](https://github.com/snbhante/snbhante.github.io/issues)
[![GitHub tag](https://img.shields.io/github/tag/snbhante/snbhante.github.io?include_prereleases=&sort=semver&color=blue)](https://github.com/snbhante/snbhante.github.io/releases/)
[![stars - snbhante.github.io](https://img.shields.io/github/stars/snbhante/snbhante.github.io?style=social)](https://github.com/snbhante/snbhante.github.io)
[![forks - snbhante.github.io](https://img.shields.io/github/forks/snbhante/snbhante.github.io?style=social)](https://github.com/snbhante/snbhante.github.io)

## Documentation

<div align="center">

[![view - Documentation](https://img.shields.io/badge/view-Documentation-blue?style=for-the-badge)](/docs/ "Go to project documentation")
[![View site - GH Pages](https://img.shields.io/badge/View_site-GH_Pages-2ea44f?style=for-the-badge)](https://snbhante.github.io/snbhante)

</div>

## License

<div align="center">

Released under [MIT](/LICENSE) by [@snbhante](https://github.com/snbhante).

<br>

**Let's connect and chat!</h3>**

<p>
<a href="mailto:sarbanandabhikkhu@gmail.com" alt="Contact me"><img src="https://raw.githubusercontent.com/jayehernandez/jayehernandez/3f5402efef9a0ae89211a6e04609558e862ca616/readme/mail-fill.svg"></a>
<a href="https://snbhante.github.io/snbhante" alt="My site"><img src="https://raw.githubusercontent.com/jayehernandez/jayehernandez/3f5402efef9a0ae89211a6e04609558e862ca616/readme/external-link-line.svg"></a>
</p>
<img src="https://raw.githubusercontent.com/jayehernandez/jayehernandez/dcd7447c179f5a1131590b6ccba2223e879ab655/readme/bottom.svg" alt="Bottom">

</div>