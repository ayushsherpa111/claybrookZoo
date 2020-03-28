const toggleBtn = document.getElementById("togBtn");
const header = document.getElementsByClassName("navbar")[0];
toggleBtn.addEventListener("click", _ => {
  header.classList.toggle('active')
});
