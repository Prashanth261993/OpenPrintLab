// Progressive enhancement: downloads and all model pages work without JavaScript.
const controls = document.querySelector(".filters");
if (controls) {
  const search = document.querySelector("#search");
  const category = document.querySelector("#category");
  const cards = [...document.querySelectorAll(".model-card")];
  const count = document.querySelector("#result-count");
  const empty = document.querySelector("#empty-state");
  const params = new URLSearchParams(location.search);
  search.value = params.get("q") || "";
  const savedCategory = params.get("category") || "";
  if ([...category.options].some(option => option.value === savedCategory)) {
    category.value = savedCategory;
  }
  function filter(updateUrl = true) {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const card of cards) {
      card.hidden = !card.dataset.search.includes(query)
        || (category.value !== "" && card.dataset.category !== category.value);
      if (!card.hidden) visible += 1;
    }
    count.textContent = `${visible} ${visible === 1 ? "model" : "models"} in the starter collection`;
    empty.hidden = visible !== 0;
    if (updateUrl) {
      const url = new URL(location.href);
      if (search.value) url.searchParams.set("q", search.value);
      else url.searchParams.delete("q");
      if (category.value) url.searchParams.set("category", category.value);
      else url.searchParams.delete("category");
      history.replaceState(null, "", url);
    }
  }
  search.addEventListener("input", () => filter());
  category.addEventListener("change", () => filter());
  document.querySelector("#clear").addEventListener("click", () => {
    search.value = "";
    category.value = "";
    filter();
    search.focus();
  });
  controls.hidden = false;
  filter(false);
}
