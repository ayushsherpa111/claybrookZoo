try {
  const canvas = document.getElementById("pie");
  const ctx = canvas.getContext("2d");

  const chart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Mammal", "Reptile", "Birds", "Amphibians"],
      datasets: [
        {
          label: "# of Votes",
          data: [12, 19, 3, 5],
          backgroundColor: [
            "rgba(255, 99, 132)",
            "rgba(54, 162, 235)",
            "rgba(255, 206, 86)",
            "rgba(75, 192, 192)"
          ]
        }
      ]
    },
    options: {
      responsive: true,
      legend: {
        labels: {
          fontColor: "white",
          fontSize: 15,
          padding: 10
        },
        position: "right"
      }
    }
  });
} catch {
  console.log("FORM BEING DISPLAYED");
}
const modal = document.getElementsByClassName("modal")[0];
const background = document.getElementsByClassName("modal-background")[0];

function displayModal() {
  modal.classList.toggle("is-active");
}

window.addEventListener("click", e => {
  if (e.target == background) {
    modal.classList.remove("is-active");
  }
});

function addAnimal(animal) {
  console.log(animal);
  fetch(`/staff/animals/${animal}`, {
    method: "GET",
    redirect: "follow"
  }).then(e => {
    window.location = e.url;
    console.log(e);
  });
}
