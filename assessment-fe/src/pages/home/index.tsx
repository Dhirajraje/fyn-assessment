import { ArrowTrendingUpIcon, BanknotesIcon, CalculatorIcon, CircleStackIcon, ClockIcon, UserIcon } from "@heroicons/react/24/solid"
import { NavLink, Outlet } from "react-router-dom"

export default function HomeWrap() {
    const navigations = [{
        name: "Calculations",
        path: "/home/calculation",
        icon: <CalculatorIcon className="w-5 h-5 text-current" />
    },
    {
        name: "Base Price",
        path: "/home/base-price-config",
        icon: <CircleStackIcon className="w-5 h-5 text-current" />
    },
    {
        name: "Additional Price",
        path: "/home/additional-price-configs",
        icon: <BanknotesIcon className="w-5 h-5 text-current" />
    },
    {
        name: "Time Multiplier",
        path: "/home/time-multiplier-configs",
        icon: <ArrowTrendingUpIcon className="w-5 h-5 text-current" />
    },
    {
        name: "Waiting Charges",
        path: "/home/waiting-charge-configs",
        icon: <ClockIcon className="w-5 h-5 text-current" />
    },
    {
        name: "Account",
        path: "/home/account",
        icon: <UserIcon className="w-5 h-5 text-current" />
    }]
    return <div className="w-screen bg-slate-50 h-screen flex flex-col overflow-auto">
        <h1 className="text-xl max-w-7xl mx-auto w-full px-2 pt-2 sm:text-2xl md:text-3xl text-indigo-600 font-bold">Charge calculation app</h1>
        <div className="max-w-7xl mx-auto w-full p-2">
            <div className="p-2 flex gap-2 bg-slate-300 w-min rounded-lg">
                {
                    navigations.map((el, index) => {
                        return <NavLink key={index} to={el.path} title={el.name} className={({ isActive }) => `p-1.5 font-bold whitespace-nowrap rounded-sm inline-flex items-center gap-2 ${isActive ? " bg-white shadow text-indigo-600 ring-indigo-600 ring-2 ring-offset-2" : " "}`}>
                            {el.icon ?? ''}
                            <span className=" hidden md:block" >{el.name}</span>
                        </NavLink>
                    })
                }
            </div>
        </div>
        <div className="max-w-7xl mx-auto w-full p-2">
            <Outlet />
        </div>
    </div>
}