const userTable = document.getElementsByClassName("table")[0];
console.log(userTable.childElementCount);

function archive(user) {
  console.log("archiving ", user);
}

function approve(row, email, role) {
  const index = row.parentNode.parentNode.rowIndex;
  if(userTable.tBodies[0].childElementCount > 0){
    fetch("/eval", {
      method: "POST",
      mode: "same-origin",
      headers: {
        "Content-Type": "application/json"
      },
      redirect: "follow",
      body: JSON.stringify({ email, role })
    })
      .then(res => res.json())
      .then(confirm => {
        userTable.deleteRow(index);
        console.log(confirm);
      })
      .catch(err => {
        console.error(err);
      });
  }

}
