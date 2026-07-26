import { BrowserRouter, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import { RequireAuth } from './components/RequireAuth'
import { RequireAdmin } from './components/RequireAdmin'
import { AdminLayout } from './components/admin/AdminLayout'
import { FrontLayout } from './components/front/FrontLayout'
import { LoginPage } from './pages/auth/LoginPage'
import { RegisterPage } from './pages/auth/RegisterPage'

import { HomePage } from './pages/front/HomePage'
import { BikeListPage as FrontBikeListPage } from './pages/front/bikes/BikeListPage'
import { BikeDetailsPage as FrontBikeDetailsPage } from './pages/front/bikes/BikeDetailsPage'
import { ManufacturerListPage as FrontManufacturerListPage } from './pages/front/manufacturers/ManufacturerListPage'
import { ManufacturerDetailsPage as FrontManufacturerDetailsPage } from './pages/front/manufacturers/ManufacturerDetailsPage'
import { CartStep1Page } from './pages/front/cart/CartStep1Page'
import { CartStep2Page } from './pages/front/cart/CartStep2Page'
import { PaymentProviderPage } from './pages/front/cart/PaymentProviderPage'
import { PaymentResultPage } from './pages/front/cart/PaymentResultPage'
import { OrderDetailsPage } from './pages/front/order/OrderDetailsPage'

import { AdminDashboardPage } from './pages/admin/AdminDashboardPage'
import { BikeListPage } from './pages/admin/bikes/BikeListPage'
import { BikeCreatePage } from './pages/admin/bikes/BikeCreatePage'
import { BikeDetailsPage } from './pages/admin/bikes/BikeDetailsPage'
import { BikeEditPage } from './pages/admin/bikes/BikeEditPage'
import { ManufacturerListPage } from './pages/admin/manufacturers/ManufacturerListPage'
import { ManufacturerCreatePage } from './pages/admin/manufacturers/ManufacturerCreatePage'
import { ManufacturerDetailsPage } from './pages/admin/manufacturers/ManufacturerDetailsPage'
import { ManufacturerEditPage } from './pages/admin/manufacturers/ManufacturerEditPage'
import { UserListPage } from './pages/admin/users/UserListPage'
import { UserCreatePage } from './pages/admin/users/UserCreatePage'
import { UserDetailsPage } from './pages/admin/users/UserDetailsPage'
import { UserEditPage } from './pages/admin/users/UserEditPage'
import { RoleListPage } from './pages/admin/roles/RoleListPage'
import { RoleCreatePage } from './pages/admin/roles/RoleCreatePage'
import { RoleDetailsPage } from './pages/admin/roles/RoleDetailsPage'
import { RoleEditPage } from './pages/admin/roles/RoleEditPage'
import { OrderListPage } from './pages/admin/orders/OrderListPage'
import { CheckoutListPage } from './pages/admin/checkouts/CheckoutListPage'
import { CartListPage } from './pages/admin/carts/CartListPage'

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route element={<FrontLayout />}>
              <Route path="/" element={<HomePage />} />
              <Route path="/auth/login" element={<LoginPage />} />
              <Route path="/auth/register" element={<RegisterPage />} />
              <Route path="/bikes" element={<FrontBikeListPage />} />
              <Route path="/bikes/:id" element={<FrontBikeDetailsPage />} />
              <Route path="/manufacturers" element={<FrontManufacturerListPage />} />
              <Route path="/manufacturers/:id" element={<FrontManufacturerDetailsPage />} />

              <Route element={<RequireAuth />}>
                <Route path="/cart/step1" element={<CartStep1Page />} />
                <Route path="/cart/step2" element={<CartStep2Page />} />
                <Route path="/cart/payment-provider" element={<PaymentProviderPage />} />
                <Route path="/cart/payment-result" element={<PaymentResultPage />} />
                <Route path="/order/details" element={<OrderDetailsPage />} />
              </Route>
            </Route>

            <Route element={<RequireAuth />}>
              <Route element={<RequireAdmin />}>
                <Route element={<AdminLayout />}>
                  <Route path="/admin" element={<AdminDashboardPage />} />

                  <Route path="/admin/bikes/list" element={<BikeListPage />} />
                  <Route path="/admin/bikes/create" element={<BikeCreatePage />} />
                  <Route path="/admin/bikes/:id/details" element={<BikeDetailsPage />} />
                  <Route path="/admin/bikes/:id/edit" element={<BikeEditPage />} />

                  <Route path="/admin/manufacturer/list" element={<ManufacturerListPage />} />
                  <Route path="/admin/manufacturer/create" element={<ManufacturerCreatePage />} />
                  <Route path="/admin/manufacturer/:id/details" element={<ManufacturerDetailsPage />} />
                  <Route path="/admin/manufacturer/:id/edit" element={<ManufacturerEditPage />} />

                  <Route path="/admin/user/list" element={<UserListPage />} />
                  <Route path="/admin/user/create" element={<UserCreatePage />} />
                  <Route path="/admin/user/:id/details" element={<UserDetailsPage />} />
                  <Route path="/admin/user/:id/edit" element={<UserEditPage />} />

                  <Route path="/admin/user/role/list" element={<RoleListPage />} />
                  <Route path="/admin/user/role/create" element={<RoleCreatePage />} />
                  <Route path="/admin/user/role/:id" element={<RoleDetailsPage />} />
                  <Route path="/admin/user/role/:id/edit" element={<RoleEditPage />} />

                  <Route path="/admin/orders/list" element={<OrderListPage />} />
                  <Route path="/admin/checkouts/list" element={<CheckoutListPage />} />
                  <Route path="/admin/carts/list" element={<CartListPage />} />
                </Route>
              </Route>
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App
