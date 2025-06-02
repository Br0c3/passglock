
  const toggle = document.getElementById("theme-toggle");
  const html = document.documentElement;

  // 1. Appliquer le thème sauvegardé au chargement
  const savedTheme = localStorage.getItem(toggle.value);
  if (savedTheme) {
    html.setAttribute("data-theme", savedTheme);
    toggle.checked = savedTheme === "dark";
  }

  // 2. Écouter le changement de toggle
  toggle.addEventListener("change", function () {
    const newTheme = toggle.checked ? "ultranoodle" : "cmyk";
    html.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  });

