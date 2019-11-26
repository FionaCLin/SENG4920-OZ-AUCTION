export function addFavorite(state, id) {
  console.log(id);
  state.favorites.push(id);
}
export function removeFavorite(state, id) {
  console.log(id);

  let index = state.favorites.indexOf(id);
  console.log(
    "index be",
    index,
    state.favorites,
    state.favorites.splice(index, 1)
  );
  state.favorites.splice(index, 1);
  console.log("index af", index, state.favorites);
}

export function updateCurrentID(state, id) {
  console.log("here is mutation_user " + id);

  state.user_id = id;
}
