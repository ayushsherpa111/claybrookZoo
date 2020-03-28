const canvas = document.getElementById("pie");
const ctx = canvas.getContext("2d");
const modal = document.getElementsByClassName("modal")[0];
const background = document.getElementsByClassName("modal-background")[0];
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

function displayModal() {
  modal.classList.toggle("is-active");
}

window.addEventListener("click", e => {
  console.log(e.target);
  if (e.target == background) {
    console.log("REMOVE MODAL");
    modal.classList.remove("is-active");
  }
});
