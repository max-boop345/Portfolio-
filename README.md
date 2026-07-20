# Maxime Novo Frelicot - Portfolio

A modern, responsive portfolio website showcasing projects in **numerical simulation, structural analysis, and algorithm visualization**.

## 📁 Structure

```
Portfolio-
├── index.html               # Homepage with hero section and 3D animation
├── about.html               # About me page (education, skills, experience)
├── projects.html            # Projects page with interactive demos
├── contact.html             # Contact page
├── assets/
│   ├── css/
│   │   └── style.css        # Global styles
│   ├── js/
│   │   ├── main.js          # Main JavaScript (navigation, etc.)
│   │   ├── threejs-bg.js    # Three.js background animation
│   │   ├── dijkstra.js      # Dijkstra's algorithm visualizer
│   │   └── ants.js          # Ant colony optimization simulation
│   ├── images/              # Project images (placeholders)
│   └── 3d/                  # 3D models (optional)
└── projects/                # Folder for your project codes (to be added)
    ├── bowling_ball/
    ├── space_elevator/
    └── rocket_trajectory/
```

## 🚀 Features

- **Responsive Design**: Works on mobile, tablet, and desktop.
- **3D Animation**: Three.js-powered bridge model on the homepage.
- **Interactive Projects**:
  - Dijkstra's Algorithm Visualizer (add nodes, edges, run algorithm).
  - Ant Colony Optimization Simulation (pheromone-based pathfinding).
- **Modern UI**: Clean, light-themed design with smooth animations.

## 🛠 Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **3D Graphics**: Three.js
- **Visualizations**: Canvas API, p5.js (for ant simulation)
- **Fonts**: Inter (Google Fonts)

## 📦 How to Deploy

### Option 1: GitHub Pages (Recommended)
1. Push this repository to your GitHub account.
2. Go to **Settings > Pages**.
3. Select **main branch** and **/ (root)** folder.
4. Your site will be live at `https://<username>.github.io/Portfolio-/`

### Option 2: Local Development
1. Clone this repository:
   ```bash
   git clone https://github.com/max-boop345/Portfolio-.git
   cd Portfolio-
   ```
2. Open `index.html` in your browser.

### Option 3: Netlify/Vercel
1. Drag and drop the repository folder to Netlify/Vercel.
2. The site will deploy automatically.

## 🔧 Customization

### Add Your Projects
1. Place your project codes in the `projects/` folder (e.g., `projects/bowling_ball/`).
2. Update the project descriptions in `projects.html`.
3. Replace placeholder images in `assets/images/` with your own visuals.

### Update Personal Info
- Edit `about.html` to update your education, skills, and experience.
- Update `contact.html` with your email, GitHub, and LinkedIn links.

### Change Theme
- Modify colors in `assets/css/style.css` (look for `:root` variables).
- Current theme: Light mode with ENPC blue (#2563EB) and green (#10B981).

## 🎨 Design Notes

- **Color Scheme**:
  - Primary: `#2563EB` (ENPC Blue)
  - Secondary: `#10B981` (Green)
  - Background: `#FFFFFF` (White)
  - Surface: `#F9FAFB` (Light Gray)

- **Typography**: Inter font family (loaded from Google Fonts).

- **Animations**: Smooth transitions and fade-ins for better UX.

## 🐛 Troubleshooting

- **Three.js not loading**: Ensure you have an internet connection (Three.js is loaded from CDN).
- **Interactive demos not working**: Check browser console for errors. Ensure JavaScript is enabled.
- **Responsive issues**: Test on different screen sizes and adjust CSS in `style.css`.

## 📜 License

This project is open-source and free to use. Feel free to customize it for your own portfolio!

---

**Made with ❤️ for Maxime Novo Frelicot**
