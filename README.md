# VANSH AI ROBOT LAB v2.0

An interactive, futuristic developer portfolio featuring a procedural 3D robot, animated cyber-forest environment, robot control deck, AI/cybersecurity modes, and a project archive.

**Owner:** Vansh Bakshi  
**GitHub:** https://github.com/VanshBakshi  
**Live site target:** https://vanshbakshi.github.io/

## Features

- Interactive 3D robot built from Three.js geometry — no external robot model required.
- Two real-time 3D viewports: hero display and full control lab.
- Animated robot idle movement, glowing eyes, AI core, floating particles, and orbiting forest.
- Three visual modes: Forest, Cyber, and Neural.
- System scan animation, AI-core pulse, animation toggle, and camera reset.
- Responsive layout for desktop, tablet, and mobile.
- Accessible labels, reduced-motion CSS support, and dynamic system log.
- GitHub Pages friendly: static HTML/CSS/JavaScript, no build step.

## Run locally

### Option 1 — VS Code Live Server
1. Extract the ZIP and open the `vansh-ai-robot-lab-v2` folder in VS Code.
2. Install the **Live Server** extension if you do not have it.
3. Right-click `index.html` → **Open with Live Server**.

### Option 2 — Python local server
Open PowerShell in the project folder and run:

```powershell
py -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

> Because the project uses JavaScript modules and Three.js from a CDN, do not open `index.html` directly with a `file://` URL. Use a local server.

## Deploy to GitHub Pages

### Recommended: use your existing user-site repository
Your GitHub user-site repository is normally named **`VanshBakshi.github.io`**.

1. Open or create the repository: https://github.com/VanshBakshi/VanshBakshi.github.io
2. Upload the contents of this project folder to the repository root. Make sure `index.html` is at the root (not nested inside another folder).
3. Commit the files to the `main` branch.
4. In the repository, open **Settings → Pages**.
5. Under **Build and deployment**, select **Deploy from a branch**.
6. Choose branch **main** and folder **/(root)**, then save.
7. Wait for the deployment to finish. Your site should appear at `https://vanshbakshi.github.io/`.

If your current website already exists in that repository, back it up before replacing files.

### Alternative: deploy from a project repository
You can put the files in a separate repository and enable GitHub Pages in its Settings → Pages. The URL will typically be `https://VanshBakshi.github.io/REPOSITORY-NAME/`.

## Connect it to your GitHub profile README

Keep your profile README in the `VanshBakshi` repository and update the robot-lab button to point to:

```html
<a href="https://vanshbakshi.github.io/">
  <img src="https://img.shields.io/badge/ENTER_VANSH_AI_ROBOT_LAB-00E5FF?style=for-the-badge&labelColor=05070B" alt="Enter VANSH AI Robot Lab">
</a>
```

## Customization

- **Name and text:** edit `index.html`.
- **Colors and responsive layout:** edit CSS variables at the top of `style.css`.
- **Robot geometry, lighting, environment, animation, and controls:** edit `robot.js`.
- **Projects:** edit the project cards in `index.html` and replace their generic repository links with the direct URL of each public project.
- **Three.js version:** the import map in `index.html` pins Three.js to `0.170.0`.

## Notes

- The robot is a real-time 3D scene, not a static picture. Drag inside the large lab viewport to rotate; scroll to zoom.
- “4D-style” means 3D graphics animated over time; it does not mean a fourth spatial dimension.
- This is a frontend visual demo. The scan and AI-core buttons trigger visual effects and logs; they do not run a real AI model or perform actual cybersecurity scanning.
- The page needs an internet connection to load Three.js and Google Fonts from their CDNs.
- If the 3D scene does not appear, use a modern browser with WebGL enabled and check the browser console for network errors.

## File structure

```text
vansh-ai-robot-lab-v2/
├── index.html
├── style.css
├── robot.js
└── README.md
```

**Build → Learn → Improve. Keep Moving Forward.**
