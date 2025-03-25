// eslint-disable-next-line no-unused-vars
import { create } from "zustand";
import { mountStoreDevtool } from "simple-zustand-devtools";

const useAuthStore = create((set, get) => ({
  allUserData: null,
  loading: false,

  //keep track te userit
  //user:()=>{(
  // user_id: get().allUserData?.user_id || null,
  //   username: get().allUserData?.user
  // )},

  user: () => ({
    user_id: get().allUserData?.user_id || null,
    username: get().allUserData?.username || null, //nese ska user e kthen null
  }),

  setUser: (user) =>
    set({
      allUserData: user,
    }),

  setLoading: (loading) => set({ loading }), //Loading

  isLoggedIn: () => get().allUserData !== null,
}));

if (import.meta.env.DEV) {
  mountStoreDevtool("Store", useAuthStore);
}
//let developers to insepct statate of the authentifaction store using dev tools

export { useAuthStore };
