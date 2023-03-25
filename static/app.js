$("#show").click(showCupcakes);

async function showCupcakes() {
  $("#cupcakes").html("");
  const response = await axios.get("/api/cupcakes");
  const cupcakes = response.data.cupcakes;
  for (let cupcake of cupcakes) {
    console.log(`${cupcake.size} ${cupcake.flavor} cupcake`);
    $("#cupcakes")
      .append(`<li class="list-group-item"><img src="${cupcake.image}">
    ${cupcake.size} ${cupcake.flavor} cupcake</li>`);
  }
}

$("#add-cupcake").click(async function (e) {
  e.preventDefault();
  const flavor = $("#flavor").val();
  const size = $("#size").val();
  const rating = $("#rating").val();
  const image = $("#image").val();
  const data = {
    flavor: flavor,
    size: size,
    rating: rating,
    image: image,
  };
  const response = await axios.post("/api/cupcakes", data);
  console.log(response);
  showCupcakes();
});
