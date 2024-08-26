import { createBrowserRouter } from 'react-router-dom'
import App from '../App'
import Home from '../components/pages/Home'
import Error from '../components/errors/Error'
import ProductionForm from '../components/production/ProductionForm'
import ProductionDetail from '../components/production/ProductionDetail'
import ProductionEdit from '../components/production/ProductionEdit'
import Registration from '../components/auth/Registration'

export const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        errorElement: <Error />,
        children: [
            {
                index: true,
                element: <Home />
            },
            {
                path: "registration",
                element: <Registration />
            },
            {
                path: "productions/new",
                element: <ProductionForm />
            },
            {
                path: "productions/:projectId/edit",
                element: <ProductionEdit />
            },
            {
                path: "/productions/:projectId",
                element: <ProductionDetail />
            }
        ]
    }
])