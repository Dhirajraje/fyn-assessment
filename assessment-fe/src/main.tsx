import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import { Navigate, RouterProvider, createBrowserRouter } from 'react-router-dom'
import Login from './pages/login';
import HomeWrap from './pages/home';
import Calculation from './pages/home/calculation';
import BasePriceConfig from './pages/home/base-price-config';
import AdditonalPriceConfig from './pages/home/additional-price-config';
import TimeMultiplierConfig from './pages/home/time-multiplier-config';
import WaitingChargeConfig from './pages/home/waiting-charge-config';
import Account from './pages/home/account';
import { Toaster } from 'react-hot-toast'
import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'


const queryClient = new QueryClient()

const _token = localStorage.getItem('token')

const router = createBrowserRouter([
  {
    path: "",
    element: <Navigate to={_token?'home/calculation':'login'} />

  },
  {
    path: 'login',
    element: <Login />
  },
  {
    path: 'home',
    element: <HomeWrap />,
    children: [
      {
        path: '',
        element: <Navigate to='calculation' />
      },
      {
        path: 'calculation',
        element: <Calculation />
      },
      {
        path: 'base-price-config',
        element: <BasePriceConfig />
      },
      {
        path: 'additional-price-configs',
        element: <AdditonalPriceConfig />
      },
      {
        path: 'time-multiplier-configs',
        element: <TimeMultiplierConfig />
      },
      {
        path: 'waiting-charge-configs',
        element: <WaitingChargeConfig />
      },
      {
        path: 'account',
        element: <Account />
      }
    ]
  }
]);


ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>

      {/* <Login /> */}
      <Toaster />
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
)
