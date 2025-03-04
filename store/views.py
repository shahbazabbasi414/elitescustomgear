from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.contrib.auth import logout
from store.models.product import Product
from store.models.orders import Order
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
from django.conf.urls import handler404
from .models.contact import Contact
from .models import Customer
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer





class index(View):
    def post(self, request):
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})

        if product_id:
            quantity = cart.get(product_id, 0)

            if remove:  # If the remove flag is set
                if quantity <= 1:
                    cart.pop(product_id)
                else:
                    cart[product_id] = quantity - 1
            else:  # Increment quantity
                cart[product_id] = quantity + 1

            # Ensure cart item is removed if quantity is 0
            if product_id in cart and cart[product_id] <= 0:
                cart.pop(product_id)

        request.session['cart'] = cart
        return redirect('index')

    def get(self, request):
        products = None
        categories = Category.get_all_category()
        parent_categories = categories.filter(parent__isnull=True)

        products = Product.objects.filter(category__in=parent_categories)

        customer = None
        if 'customer_id' in request.session:
            customer = Customer.objects.filter(id=request.session['customer_id']).first()

        cart = request.session.get('cart', {})

        data = {
            'Categories': parent_categories, 
            'products': products, 
            'Customer': customer,
            'cart': cart 
        }

        return render(request, 'index.html', data)



def signup(request):
    if request.method == 'POST':
        postData = request.POST
        first_name = postData.get('first_name')
        last_name = postData.get('last_name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        re_password = postData.get('re_password')
        security_question_1 = postData.get('security_question_1')
        security_question_2 = postData.get('security_question_2')
        security_question_3 = postData.get('security_question_3')

        # Validate input
        if not all([first_name, last_name, phone, email, password, re_password, security_question_1, security_question_2, security_question_3]):
            return render(request, 'signup.html', {'All_Required': True})

        if password != re_password:
            return render(request, 'signup.html', {'password_mismatch': True})

        if Customer.objects.filter(email=email).exists() or Customer.objects.filter(phone=phone).exists():
            return render(request, 'signup.html', {'email_phone_match': True})

        # Create new customer
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone=phone,
            security_question_1=security_question_1,
            security_question_2=security_question_2,
            security_question_3=security_question_3
        )
        customer.save()
        request.session['customer_id'] = customer.id
        request.session['email'] = email

        return redirect('index')
    
    else:
        categories = Category.get_all_category()
        parent_categories = categories.filter(parent__isnull=True)  # Only parent categories

        data = {
            'Categories': parent_categories  # Pass parent categories to the template
        }

        return render(request, 'signup.html', data)




def password_recovery(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        security_question_1 = request.POST.get('security_question_1')
        security_question_2 = request.POST.get('security_question_2')
        security_question_3 = request.POST.get('security_question_3')

        customer = Customer.get_customer_by_email(email)
        if customer:
            if (customer.security_question_1 == security_question_1 and
                customer.security_question_2 == security_question_2 and
                customer.security_question_3 == security_question_3):
                return render(request, 'reset_password.html', {'email': email})
            else:
                return render(request, 'password_recovery.html', {'security_mismatch': True})
        else:
            return render(request, 'password_recovery.html', {'email_not_found': True})
    else:
        return render(request, 'password_recovery.html')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            customer = Customer.get_customer_by_email(email)
            if customer:
                customer.password = make_password(new_password)
                customer.save()
                return redirect('login')
        else:
            return render(request, 'reset_password.html', {'password_mismatch': True, 'email': email})
    else:
        return redirect('password_recovery')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        return_url = request.POST.get('return_url', '/')

        customer = Customer.get_customer_by_email(email)
        error_message = None

        if customer:
            # Check the hashed password
            if check_password(password, customer.password):
                request.session['customer_id'] = customer.id 
                request.session['email'] = email 
                return redirect(return_url)
            else:
                error_message = 'Wrong Email or Password'
                return render(request, 'login.html', {'error_message': True, 'return_url': return_url})  
        else:
            error_message = 'Wrong Email or Password'
            return render(request, 'login.html', {'error_message': True, 'return_url': return_url}) 

    else:
        categories = Category.get_all_category()
        parent_categories = categories.filter(parent__isnull=True)
        
        return_url = request.GET.get('return_url', '/')
        return render(request, 'login.html', {
            'Categories': parent_categories,
            'return_url': return_url
        })



def logout_view(request):
    logout(request)
    request.session.flush() 
    return redirect('login')

def Cart(request):
    cart = request.session.get('cart', {})
    # print("Cart data:", cart)
    # return JsonResponse({"status": "POST data received", "data": request.POST.dict()})
    
    # Extract product IDs from cart keys
    product_ids = [key.split('-')[0] for key in cart.keys()]
    
    products = Product.get_Products_by_id(product_ids)
    categories = Category.get_all_category()
    parent_categories = categories.filter(parent__isnull=True)
    
    customer = None
    if 'customer_id' in request.session:
        customer = Customer.objects.filter(id=request.session['customer_id']).first()
    
    # Calculate total price
    cart_items = []
    cart_total = 0  # Initialize total variable
    for key, quantity in cart.items():
        product_id, color,fabric, material, size, customization, product_type, gsm, chosequantity = key.split('-')
        product = next((p for p in products if p.id == int(product_id)), None)
        if product:
            item_total = product.price * quantity  # Calculate total for this item
            cart_total += item_total  # Add to total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'color': color,
                'fabric':fabric,
                'material': material,
                'size': size,
                'customization': customization,
                'type': product_type,
                'gsm': gsm,
                'chosequantity': chosequantity,
                'item_total': item_total,  # Optionally store item total for each item
            })
    
    return render(request, 'cart.html', {
        'cart_items': cart_items, 
        'products': products, 
        'Customer': customer, 
        'Categories': parent_categories,
        'cart_total': cart_total  # Pass the total to the template
    })


def delete_cart(request):
    if request.method == "POST":
        # Clear the cart from the session
        if 'cart' in request.session:
            del request.session['cart']
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseBadRequest("Invalid request method")



class OrderView(View):
    def get(self, request):
        customer_id = request.session.get('customer_id')
        categories = Category.get_all_category()
        parent_categories = categories.filter(parent__isnull=True)
        if not customer_id:
            return redirect('login')
        customer = Customer.objects.get(id=customer_id)
        orders = Order.get_order_by_customer(customer)
        # print(orders)

        return render(request, 'order.html', {'orders': orders, 'Customer': customer, 'Categories': parent_categories,})

class checkOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        detail = request.POST.get('detail')
        return_url = request.POST.get('return_url', 'cart')
        customer_id = request.session.get('customer_id')
        cart = request.session.get('cart', {})
        
        if not customer_id:
            return redirect(f'/login/?return_url={return_url}')

        # Extract product IDs and attributes from cart keys
        for key, quantity in cart.items():
            product_id, color,fabric, material, size, customization, product_type, gsm, chosequantity = key.split('-')
            product = Product.objects.get(id=int(product_id))

            if quantity > 0:
                order = Order(
                    customer=Customer(id=customer_id),
                    product=product,
                    price=product.price,
                    address=address,
                    phone=phone,
                    detail=detail,
                    quantity=quantity,
                    color=color,
                    fabric=fabric,
                    material=material,
                    size=size,
                    customization=customization,
                    type=product_type,
                    gsm=gsm,
                    chosequantity=chosequantity,
                )
                order.placeOrder()

        request.session['cart'] = {}
        return redirect(return_url)

    


def products(request):
    if request.method == "POST":
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})

        if product_id:
            quantity = cart.get(product_id, 0)

            if remove:
                if quantity <= 1:
                    cart.pop(product_id)
                else:
                    cart[product_id] = quantity - 1
            else:
                cart[product_id] = quantity + 1

            if cart.get(product_id) == 0:
                cart.pop(product_id)

        request.session['cart'] = cart
        return redirect('products')

    else:
        products = None
        categories = Category.get_all_category()
        category_id = request.GET.get('category')

        if category_id:
            selected_category = Category.objects.filter(id=category_id).first()
            if selected_category:
                child_categories = selected_category.get_children()
                all_categories = [selected_category] + list(child_categories)
                products = Product.objects.filter(category__in=all_categories)
        else:
            products = Product.get_all_products()

        customer = None
        if 'customer_id' in request.session:
            customer = Customer.objects.filter(id=request.session['customer_id']).first()

        cart = request.session.get('cart', {})

        parent_categories = categories.filter(parent__isnull=True)

        data = {
            'Categories': parent_categories,
            'products': products,
            'Customer': customer,
            'cart': cart
        }

        return render(request, 'Products.html', data)



def cartPage(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    materials = product.materials.all()
    sizes = product.sizes.all()
    customizations = product.customizations.all()
    types = product.types.all()
    colors = product.colors.all()
    fabrics = product.fabrics.all()
    gsms = product.gsms.all()
    chosequantitys = product.chosequantitys.all()
    
    cart = request.session.get('cart', {})
    categories = Category.get_all_category()
    parent_categories = categories.filter(parent__isnull=True)
    customer = None
    if 'customer_id' in request.session:
        customer = Customer.objects.filter(id=request.session['customer_id']).first()
    
    # Check if the request is for editing a cart item
    edit = request.GET.get('edit', False)
    if edit:
        color = request.GET.get('color', '')
        fabric = request.GET.get('fabric', '')
        material = request.GET.get('material', '')
        size = request.GET.get('size', '')
        customization = request.GET.get('customization', '')
        product_type = request.GET.get('type', '')
        gsm = request.GET.get('gsm', '')
        chosequantity = request.GET.get('chosequantity', '')
        
        # Pass the current options to the template
        return render(request, 'product-details-page.html', {
            'product': product,
            'cart': cart,
            'Categories': parent_categories,
            'Customer': customer,
            'color': colors,
            'fabric': fabrics,
            'material': materials,
            'size': sizes,
            'customization': customizations,
            'type': types,
            'gsms': gsms,
            'chosequantity': chosequantitys,
            'edit': True,
            'selected_color': color,
            'selected_fabric': fabric,
            'selected_material': material,
            'selected_size': size,
            'selected_customization': customization,
            'selected_type': product_type,
            'selected_gsm': gsm,
            'selected_chosequantity': chosequantity,
        })
    
    return render(request, 'product-details-page.html', {
        'product': product,
        'cart': cart,
        'Categories': parent_categories,
        'Customer': customer,
        'color': colors,
        'fabric': fabrics,
        'material': materials,
        'size': sizes,
        'customization': customizations,
        'type': types,
        'gsms': gsms,
        'chosequantity': chosequantitys,
    })


def update_cart(request):
    if request.method == "POST":
        # Get POST data
        product_id = request.POST.get('product')
        remove = request.POST.get('remove')

        # Ensure product_id is provided
        if not product_id:
            return HttpResponseBadRequest("Product ID is missing")

        # Get or initialize cart from the session
        cart = request.session.get('cart', {})

        # Extract additional product options from the form
        color = request.POST.get('color')
        fabric = request.POST.get('fabric')
        material = request.POST.get('material')
        size = request.POST.get('size')
        customization = request.POST.get('customization')
        product_type = request.POST.get('type')
        gsm = request.POST.get('gsm')
        chosequantity = request.POST.get('chosequantity')

        # Build a key to store product with options
        product_key = f"{product_id}-{color or ''}-{fabric or ''}-{material or ''}-{size or ''}-{customization or ''}-{product_type or ''}-{gsm or ''}-{chosequantity or ''}"

        # Remove the product from cart if `remove` is provided
        if remove:
            if product_key in cart:
                del cart[product_key]
        else:
            # If editing, remove the old item and add the new one
            old_product_key = request.POST.get('old_product_key')
            if old_product_key and old_product_key in cart:
                del cart[old_product_key]
            
            if product_key in cart:
                cart[product_key] += 1
            else:
                cart[product_key] = 1  # Initialize product in cart with quantity 1

        # Save the updated cart in the session
        request.session['cart'] = cart

        # Redirect back to the page or a fallback URL
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return HttpResponseBadRequest("Invalid request method")

def about(request):
    categories = Category.get_all_category()
    category_id = request.GET.get('category')
    parent_categories = categories.filter(parent__isnull=True)
    products = None

    if category_id:
        products = Product.get_all_products_by_id(category_id)
    else:
        products = Product.get_all_products()

    customer = None
    if 'customer_id' in request.session:
        customer = Customer.objects.filter(id=request.session['customer_id']).first()

    cart = request.session.get('cart', {})

    context = {
        'Categories': parent_categories,
        'products': products,
        'Customer': customer,
        'cart': cart
    }

    return render(request, 'about.html', context)


def process(request):
    categories = Category.get_all_category()
    parent_categories = categories.filter(parent__isnull=True)
    category_id = request.GET.get('category')
    products = None

    if category_id:
        products = Product.get_all_products_by_id(category_id)
    else:
        products = Product.get_all_products()

    customer = None
    if 'customer_id' in request.session:
        customer = Customer.objects.filter(id=request.session['customer_id']).first()

    cart = request.session.get('cart', {})

    context = {
        'Categories': parent_categories,
        'products': products,
        'Customer': customer,
        'cart': cart
    }

    return render(request, 'process.html', context)


def fabric(request):
    categories = Category.get_all_category()
    parent_categories = categories.filter(parent__isnull=True)
    category_id = request.GET.get('category')
    products = None

    if category_id:
        products = Product.get_all_products_by_id(category_id)
    else:
        products = Product.get_all_products()

    customer = None
    if 'customer_id' in request.session:
        customer = Customer.objects.filter(id=request.session['customer_id']).first()

    cart = request.session.get('cart', {})

    context = {
        'Categories': parent_categories,
        'products': products,
        'Customer': customer,
        'cart': cart
    }

    return render(request, 'fabric.html', context)
@csrf_exempt  # Temporarily disable CSRF for testing (remove in production)
def contact(request):
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Save to database
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()

            # Return success response
            return JsonResponse({'status': 'success', 'message': 'Your message has been sent. Thank you!'})
        except Exception as e:
            # Return error response
            return JsonResponse({'status': 'error', 'message': 'There was an error sending your message. Please try again later.'}, status=500)

    # If it's a GET request, render the contact page
    categories = Category.get_all_category()
    parent_categories = categories.filter(parent__isnull=True)
    context = {
        'Categories': parent_categories,
        'products': products,  # Ensure 'products' is defined
    }
    return render(request, 'contact.html', context)


def support(request):
    categories = Category.get_all_category()
    parent_categories = categories.filter(parent__isnull=True)
    category_id = request.GET.get('category')
    products = None

    if category_id:
        products = Product.get_all_products_by_id(category_id)
    else:
        products = Product.get_all_products()

    customer = None
    if 'customer_id' in request.session:
        customer = Customer.objects.filter(id=request.session['customer_id']).first()

    cart = request.session.get('cart', {})

    context = {
        'Categories': parent_categories,
        'products': products,
        'Customer': customer,
        'cart': cart
    }
    return render(request,'support.html',context )

def customization(request):
    categories = Category.get_all_category()
    parent_categories = categories.filter(parent__isnull=True)
    category_id = request.GET.get('category')
    products = None

    if category_id:
        products = Product.get_all_products_by_id(category_id)
    else:
        products = Product.get_all_products()

    customer = None
    if 'customer_id' in request.session:
        customer = Customer.objects.filter(id=request.session['customer_id']).first()

    cart = request.session.get('cart', {})

    context = {
        'Categories': parent_categories,
        'products': products,
        'Customer': customer,
        'cart': cart
    }

    return render(request, 'customization.html', context)


