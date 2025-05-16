const user = JSON.parse(localStorage.getItem("user"));

export const userId = user?.id || null;