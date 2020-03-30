const image = document.getElementsByClassName("file-input")[0];
const imageCount = document.getElementsByClassName("file-label")[1];
const fileName = document.getElementsByClassName("file-name")[0];
console.log(image);

image.onchange = () => {
  imageCount.textContent = `Files selected: ${image.files.length}`;
  if(image.files.length == 0){
    fileName.textContent = "No Image File Selected";
  }else{
    fileName.textContent = image.files[0].name;
  }
};
