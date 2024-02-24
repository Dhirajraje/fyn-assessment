import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import api from "@/utils/axios-instance";
import { EyeIcon, PencilIcon } from "@heroicons/react/24/solid";
import { Label } from "@radix-ui/react-label";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";


async function getTimeMultipler() {
    return await api.get('master/tmf-master/')
}

export default function TimeMultiplierConfig() {
    const query = useQuery({ queryKey: ['time-multiplier-factor'], queryFn: getTimeMultipler })
    const [modalState, setModalState] = useState<{ isOpen: boolean, data: any }>({
        isOpen: false,
        data: null
    })
    const [history, setHistory] = useState<number | undefined>()
    return <div className="flex flex-col gap-2 w-full max-w-7xl p-2">
        {
            query.isLoading ? <div className="p-10 flex w-full justify-center items-center">
                <div className="w-4 h-4 bg-indigo-600 rounded-full animate-ping"></div>
            </div> : query.isError ? <div className="text-red-400">Something went wrong</div> : <>
                <div className="flex gap-2 items-center">
                    <h2 className="text-lg font-semibold flex-grow">Time Multipler</h2>
                    <Button onClick={_ => {
                        setModalState({
                            isOpen: true,
                            data: null
                        })
                    }}>Add New</Button>
                </div>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="w-[100px]">id</TableHead>
                            <TableHead>Multiplier Factor</TableHead>
                            <TableHead>Time Clamp</TableHead>
                            <TableHead>Created By</TableHead>
                            <TableHead>Created On</TableHead>
                            <TableHead className="">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {query.data?.data.data.map((entry: any) => (
                            <TableRow key={entry.id}>
                                <TableCell className="font-medium">{entry.id}</TableCell>
                                <TableCell>{entry.multiplier}</TableCell>
                                <TableCell>{entry.time_clip}</TableCell>
                                <TableCell>{entry.created_by.username}</TableCell>
                                <TableCell>{entry.created_on ? new Date(entry.created_on.split('.')[0]).toLocaleDateString('en-GB') : ''}</TableCell>
                                <TableCell className=" justify-end inline-flex gap-2">
                                    <Button onClick={_ => {
                                        setHistory(entry.id)
                                    }}><EyeIcon className="w-4 h-4" /></Button>
                                    <Button onClick={_ => {
                                        setModalState({
                                            isOpen: true,
                                            data: entry
                                        })
                                    }}><PencilIcon className="w-4 h-4" /></Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table></>
        }
        {
            modalState.isOpen ?
                <Modal modalState={modalState} setModalState={setModalState} />
                : null
        }
        {
            history ?
                <HistoryModal id={history} closeHistoryModal={() => setHistory(undefined)} />
                : null
        }
    </div>
}

function Modal({ setModalState, modalState }: { setModalState: Function, modalState: { isOpen: boolean, data: any } }) {

    async function saveAdditionalPrice() {
        if (!modalState.data.id) {
            const _data_to_add = {
                multiplier: modalState.data.multiplier,
                time_clip: modalState.data.time_clip,
            }
            await api.post('master/tmf-master/', _data_to_add)
            setModalState({ isOpen: false, data: null })
        }
        else {
            const _data_to_update = {
                id: modalState.data.id,
                multiplier: modalState.data.multiplier,
                time_clip: modalState.data.time_clip,
            }
            await api.patch('master/tmf-master/', _data_to_update)
            setModalState({ isOpen: false, data: null })

        }
    }
    // Mutations
    const queryClient = useQueryClient()

    const mutation = useMutation({
        mutationFn: saveAdditionalPrice,
        onSuccess: () => {
            // Invalidate and refetch
            queryClient.invalidateQueries({ queryKey: ['time-multiplier-factor'] })
        },
    })

    return <div className="absolute bg-slate-500/30 top-0 p-2 left-0 h-screen w-screen flex justify-center items-center">
        <div className="rounded-md bg-white max-w-md w-full shadow p-4 flex flex-col">
            <h2 className="text-lg border-b font-semibold">
                Multiplier Factor
            </h2>
            <div className="flex-grow overflow-visible">
                <div className="grid w-full items-center gap-1.5 p-1">
                    <Label htmlFor="multiplier-factor">Multiplier Factor</Label>
                    <Input value={modalState.data?.multiplier} onChange={e => {
                        setModalState({
                            ...modalState,
                            data: {
                                ...modalState.data ?? {},
                                multiplier: e.target.value
                            }
                        })
                    }} type="number" id="multiplier-factor" placeholder="Multiplier Factor" />

                </div>
                <div className="grid w-full items-center gap-1.5 p-1">
                    <Label htmlFor="time-clip">Time Clamp</Label>
                    <Input value={modalState.data?.time_clip} onChange={e => {
                        setModalState({
                            ...modalState,
                            data: {
                                ...modalState?.data ?? {},
                                time_clip: e.target.value
                            }
                        })
                    }} type="number" id="time-clip" placeholder="Time Clamp" />

                </div>
            </div>
            <div className="flex justify-end gap-2">
                <Button onClick={_ => {
                    setModalState({ isOpen: false, data: null })
                }} variant="outline">Cancel</Button>
                <Button onClick={_ => {
                    mutation.mutate()
                }}>Save</Button>
            </div>
        </div>
    </div>;
}


function HistoryModal({ id, closeHistoryModal }: { id: number, closeHistoryModal: Function }) {

    async function getAdditionalPriceHistory() {
        return await api.get('master/audits/', {
            params: {
                audit_type: 'TMF',
                audit_tx_id: id
            }
        })
    }
    const query = useQuery({ queryKey: ['audit-history', 'TMF', id], queryFn: getAdditionalPriceHistory })

    return <div className="absolute bg-slate-500/30 top-0 p-2 left-0 h-screen w-screen flex justify-center items-center">
        <div className="rounded-md max-h-96 bg-white max-w-md w-full shadow p-4 flex flex-col">
            <h2 className="text-lg border-b font-semibold">
                Audit Histroy
            </h2>
            <div className="flex-grow flex flex-col gap-2 p-2 overflow-auto">
                {query.isLoading ? <div className="p-10 flex w-full justify-center items-center">
                    <div className="w-4 h-4 bg-indigo-600 rounded-full animate-ping"></div>
                </div> : query.isError ? <div className="text-red-400">Something went wrong</div> :
                    <>
                        {
                            query.data?.data.data.map((el: any, index: any) => {
                                return <div className="flex flex-col gap-2 p-2 bg-slate-100 rounded-md" key={index}>
                                    <div className="flex border-b w-full items-center justify-between">
                                        <h3 className="text-md text-slate-800 flex-grow font-medium">
                                            {el.created_by.username}
                                        </h3>
                                        <span className="text-sm">
                                            {el.created_on ? new Date(el.created_on.split('.')[0]).toLocaleDateString('en-GB') : ''}
                                        </span>
                                    </div>
                                    {
                                        // <></>
                                        // <div className="whitespace-wrap">{JSON.stringify(el)}</div>
                                        // console.log(el);

                                        Object.keys(el.data).map((_el: any, index: number) => {
                                            if(el.data[_el] == 'created_by' || el.data[_el] == 'applicable_days') return
                                            return <div key={index} className="flex justify-between">
                                                <span className="font-bold">{_el}</span>
                                                <span className="">{el.data[_el]??'-'}</span>
                                            </div>
                                        })
                                    }
                                </div>
                            })
                        }
                    </>}
            </div>
            <div className="flex justify-end gap-2">
                <Button onClick={_ => {
                    closeHistoryModal()
                }}>Close</Button>
            </div>
        </div>
    </div>;
}
