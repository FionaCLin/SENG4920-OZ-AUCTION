export function addFavorite(state, id) {
  id = Number(id);
  state.favorites.push(id);
}
export function removeFavorite(state, id) {
  let index = state.favorites.indexOf(id);

  state.favorites.splice(index, 1);
}

export function updateCurrentID(state, user) {
  for (let k of Object.keys(state)) {
    if (Object.keys(user).includes(k)) state[k] = user[k];
  }
  return state;
}

export function updateUserDetail(state, data) {
  for (let k of Object.keys(state)) {
    if (k != "user_id") state[k] = data[k];
  }
}
