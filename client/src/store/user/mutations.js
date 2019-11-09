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

// export const STORAGE_KEY = 'todos-vuejs'

// // for testing
// if (navigator.userAgent.indexOf('PhantomJS') > -1) {
//   window.localStorage.clear()
// }

// export const mutations = {
//   addTodo (state, todo) {
//     state.todos.push(todo)
//   },

//   removeTodo (state, todo) {
//     state.todos.splice(state.todos.indexOf(todo), 1)
//   },

//   editTodo (state, { todo, text = todo.text, done = todo.done }) {
//     todo.text = text
//     todo.done = done
//   }
// }
