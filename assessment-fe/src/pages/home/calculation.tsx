import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import api from "@/utils/axios-instance";
import { BanknotesIcon, CalendarIcon } from "@heroicons/react/24/solid";
import { useState } from "react";
import toast from "react-hot-toast";


function formatDate(date: Date) {
    const year = date.toLocaleString('default', { year: 'numeric' });
    const month = date.toLocaleString('default', {
        month: '2-digit',
    });
    const day = date.toLocaleString('default', { day: '2-digit' });

    return [year, month, day].join('-');
}


export default function Calculations() {
    const [date, setDate] = useState<Date>()
    const [submitAttempted, setSubmitAttempts] = useState(false)
    const [distance, setDistance] = useState()
    const [travelTime, setTravelTime] = useState()
    const [waitingTime, setWatingTime] = useState()
    const [modalState, setModalState] = useState<number | null>(null)

    async function runCalculations() {
        const _res = await api.post('master/calculations/', {
            distance_travelled: distance,
            amount_of_time_travelled: travelTime,
            waiting_time: waitingTime,
            date_of_travel: formatDate(date ?? new Date())
        })
        return _res.data.data
    }

    return <><div className="p-2 max-w-3xl flex flex-col gap-2 w-full">
        <div className="grid w-full max-w-sm items-center gap-1.5">
            <Label htmlFor="dt">Date of travel</Label>
            <Popover>
                <PopoverTrigger asChild>
                    <Button
                        variant={"outline"}
                        className={cn(
                            "justify-start text-left font-normal",
                            !date && "text-muted-foreground"
                        )}
                    >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {date ? date.toDateString() : <span>Pick a date</span>}
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                        mode="single"
                        selected={date}
                        onSelect={setDate}
                        initialFocus
                    />
                </PopoverContent>
            </Popover>
            {submitAttempted && !date ? <Label htmlFor="dt" className="text-red-400">No value selected</Label> : null}

        </div>
        <div className="grid w-full max-w-sm items-center gap-1.5">
            <Label htmlFor="dt">Distance Travelled (in KMs)</Label>
            <Input type="number" id="dt" placeholder="Distance Travelled" value={distance} onChange={(e: any) => {
                setDistance(e.target.value)
            }} />
            {submitAttempted && !distance ? <Label htmlFor="dt" className="text-red-400">Invalid Value</Label> : null}
        </div>
        <div className="grid w-full max-w-sm items-center gap-1.5">
            <Label htmlFor="ttt">Total Time Travelled (in hours)</Label>
            <Input type="number" id="ttt" placeholder="Total Time Travelled" value={travelTime} onChange={(e: any) => {
                setTravelTime(e.target.value)
            }} />
            {submitAttempted && !travelTime ? <Label htmlFor="dt" className="text-red-400">Invalid Value</Label> : null}

        </div>
        <div className="grid w-full max-w-sm items-center gap-1.5">
            <Label htmlFor="wt">Waiting Time (in minutes)</Label>
            <Input type="number" id="wt" placeholder="Waiting Time" value={waitingTime} onChange={(e: any) => {
                setWatingTime(e.target.value)
            }} />
            {submitAttempted && !waitingTime ? <Label htmlFor="dt" className="text-red-400">Invalid Value</Label> : null}

        </div>
        <div className="grid w-full max-w-sm items-center pt-2 mt-2 border-t gap-1.5">
            <Button className="bg-indigo-600"
                onClick={_ => {
                    if (!date || !distance) {
                        setSubmitAttempts(true)
                        return
                    }
                    setSubmitAttempts(false)
                    const _result = runCalculations().then((result) => {
                        setModalState(result);

                    })
                    toast.promise(_result, {
                        loading: "Loading",
                        success: "Calculations successful",
                        error: "Something went wrong"
                    })

                }}
            >Submit</Button>
        </div>
    </div>
        {
            modalState ?
                <Modal modalState={modalState} setModalState={setModalState} />
                : null
        }</>
}


function Modal({ setModalState, modalState }: { setModalState: Function, modalState: number }) {


    return <div className="absolute bg-slate-500/30 top-0 p-2 left-0 h-screen w-screen flex justify-center items-center">
        <div className="rounded-md bg-white max-w-md w-full shadow p-4 flex flex-col">
            <h2 className="text-lg border-b font-semibold">
                Total Bill
            </h2>
            <div className="flex-grow overflow-visible flex w-full h-56 justify-center items-center relative">
                <div className="absolute w-full h-full flex justify-center items-center">
                    <span className="h-48 w-48 bg-emerald-300 rounded-full flex justify-center items-center">
                        <BanknotesIcon className=" w-32 h-32 text-green-100 animate-pulse" />
                    </span>
                </div>
                <span className="z-20 text-5xl font-bold text-slate-800">₹ {modalState}</span>
            </div>
            <div className="flex justify-center gap-2">

                <Button onClick={_ => {
                    setModalState(null)
                }}>Pay and exit</Button>
            </div>
        </div>
    </div>;
}
