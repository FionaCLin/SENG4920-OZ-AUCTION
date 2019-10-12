/*
export function someAction (context) {
}
*/
import {
  axiosInstance
} from "axios";
import {
  LocalStorage
} from "quasar";

export const login = (commit, creds) => {
  axiosInstance.post("/authentication", creds).then(res => {
    console.log(res.data.accessToken);
    LocalStorage.set("token", res.data.accessToken);
  });
};

// export default {
//   addTodo({ commit }, text) {
//     commit("addTodo", {
//       text,
//       done: false
//     });
//   },

//   removeTodo({ commit }, todo) {
//     commit("removeTodo", todo);
//   },

//   toggleTodo({ commit }, todo) {
//     commit("editTodo", {
//       todo,
//       done: !todo.done
//     });
//   },

//   editTodo({ commit }, { todo, value }) {
//     commit("editTodo", {
//       todo,
//       text: value
//     });
//   },

//   toggleAll({ state, commit }, done) {
//     state.todos.forEach(todo => {
//       commit("editTodo", {
//         todo,
//         done
//       });
//     });
//   },

//   clearCompleted({ state, commit }) {
//     state.todos
//       .filter(todo => todo.done)
//       .forEach(todo => {
//         commit("removeTodo", todo);
//       });
//   }
// };
