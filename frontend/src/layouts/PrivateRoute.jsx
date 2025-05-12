import { Children, Navigate } from "react";

import { useAuthStore } from "../store/auth";

const PrivateRoute = ({ children }) => {
  const loggedIn = useAuthStore((state) => state.isLoggedIn)();

  return loggedIn ? <>{children}</> : <Navigate to="/login/" />;
};

export default PrivateRoute;

//kur e bon naj modul psh studenDashbord mes privateRoute eshte secured edhe i duhet userit mu bo login per me u qas
//
