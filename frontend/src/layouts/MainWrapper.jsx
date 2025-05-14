<<<<<<< HEAD
import { useEffect, useState } from "react";
import { setUser } from "../utils/Auth";

const MainWrapper = ({ children }) => {
  //kur thirret "projecti" vjen krejt kodi posht, nese jo
  const [loding, setLoading] = useState(true); //e gjejm nje variabel edhe eerdorimme set data

  useEffect(() => {
    const handler = async () => {
      setLoading(true);

      await setUser(); //nese krejt shkon okej per me u atentifiku e bojm setloadinf false

      setLoading(false); //ska nevoj me set data se u krys
    };
    handler();
  }, []);
  return <>{loding ? null : children}</>; //nese loading eshte complet bohet children
};

export default MainWrapper;


const MainWrapper=({children}) =>{  //kur thirret "projecti" vjen krejt kodi posht, nese jo
    const [loding,setLoading]=useState(true); //e gjejm nje variabel edhe eerdorimme set data

    useEffect(()=>{
        const handler= async()=>{
            setLoading(true);


            await setUser(); //nese krejt shkon okej per me u atentifiku e bojm setloadinf false


            setLoading(false); //ska nevoj me set data se u krys

        };
        handler();
    }, []);
    return <>{loding? null: children}</> //nese loading eshte complet bohet children
};


export default MainWrapper;
>>>>>>> 21a1b1a39e5062f1f0af7d86eecd5566a777eec4
