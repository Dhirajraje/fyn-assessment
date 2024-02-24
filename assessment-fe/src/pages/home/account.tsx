import { Button } from "@/components/ui/button";
import { ArrowUpTrayIcon } from "@heroicons/react/24/solid";
import { useNavigate } from "react-router-dom";

export default function Account(){
    const _navigate = useNavigate()
    return <div className="">
        <Button className="bg-red-400" onClick={()=>{
            localStorage.clear()
            _navigate('/login')
        }}> <ArrowUpTrayIcon className="rotate-90 w-5 h-5 mr-2" /> Logout</Button>
    </div>
}