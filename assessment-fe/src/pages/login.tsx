import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@radix-ui/react-label";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import toaster from 'react-hot-toast';
import axios from "axios";
import { BASE_URL } from "@/utils/consts";

export default function Login() {
	const _navigate = useNavigate()
	const [formData, setFormData] = useState({
		username: '',
		password: ''
	})
	const [formError, setFormError] = useState({
		username: '',
		password: ''
	})
	const [apiInProgress, setApiInProgress] = useState(false)
	return <div className="min-h-screen w-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
		<div className="relative py-3 sm:max-w-xl sm:mx-auto">
			<div
				className="absolute inset-0 bg-gradient-to-r from-indigo-300 to-indigo-600 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl">
			</div>
			<div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
				<div className="max-w-md mx-auto">
					<div>
						<h1 className="text-2xl font-semibold">Login Form with Floating Labels</h1>
					</div>
					<div className="divide-y divide-gray-200">
						<div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
							<div className="grid w-full max-w-sm items-center gap-1.5">
								<Label htmlFor="username">Username</Label>
								<Input onChange={e => {
									setFormData({ ...formData, username: e.target.value });
									let error = ''
									if (e.target.value.length < 4 || e.target.value.length > 12) {
										error = 'Username should be 4 to 12 chars long'
									}
									setFormError({ ...formError, username: error })
								}} type="username" id="username" placeholder="Username" />
								{
									formError.username ? <Label htmlFor="username" className="text-red-500">{formError.username}</Label> : ''
								}
							</div>
							<div className="grid w-full max-w-sm items-center gap-1.5">
								<Label htmlFor="password">Password</Label>
								<Input onChange={e => {
									setFormData({ ...formData, password: e.target.value });
									let error = ''
									if (e.target.value.length < 8 || e.target.value.length > 16) {
										error = 'Username should be 8 to 16 chars long';
									}
									setFormError({ ...formError, password: error })
								}} type="password" id="password" placeholder="Password" />
								{
									formError.password ? <Label htmlFor="password" className="text-red-500">{formError.password}</Label> : ''
								}
							</div>
							<div className="grid w-full max-w-sm items-center gap-1.5">
								<Button disabled={apiInProgress} onClick={_ => {
									if (formError.username || formError.password) {
										toaster.error("Please check username and password")
										return
									}
									setApiInProgress(true)
									let result = axios.post(BASE_URL + 'api/token/', formData).then(res => {
										localStorage.setItem('token', res.data.access)
										localStorage.setItem('refresh', res.data.refresh)
										_navigate('/home/calculation')
									}).finally(() => {
										setApiInProgress(false)
									})
									toaster.promise(result, {
										loading: "Loading",
										success: "Successfully logged in",
										error: "Something went wrong"
									})
									// _navigate('/home/calculation')
								}} className="bg-indigo-600" >Submit</Button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div >

}

