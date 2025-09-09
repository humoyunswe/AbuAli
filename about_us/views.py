from django.shortcuts import render

# Create your views here.

def about_us(request):
    context = {
        'title': 'Biz haqimizda',
        'page_description': 'Bizning kompaniya haqida ma\'lumot',
        'team_members': [
            {
                'name': 'John Doe',
                'position': 'CEO & Founder',
                'image_url': 'https://via.placeholder.com/150',
                'description': 'Kompaniya asoschisi va rejalashtiruvchi'
            },
            {
                'name': 'Jane Smith',
                'position': 'Lead Developer',
                'image_url': 'https://via.placeholder.com/150',
                'description': 'Ishlab chiqaruvchi jamiyatning bosh dasturlashchi'
            },
            {
                'name': 'Mike Johnson',
                'position': 'Design Director',
                'image_url': 'https://via.placeholder.com/150',
                'description': 'UI/UX dizayn jamiyatning bosh direktori'
            }
        ],
        'services': [
            {
                'title': 'Web Development',
                'icon': '💻',
                'description': 'Custom websites and web applications built with the latest technologies and best practices.'
            },
            {
                'title': 'Mobile Apps',
                'icon': '📱',
                'description': 'Native and cross-platform mobile applications designed for both iOS and Android.'
            },
            {
                'title': 'Telegram Bots',
                'icon': '🤖',
                'description': 'Smart and efficient Telegram bots for business automation and customer service.'
            },
            {
                'title': 'UI/UX Design',
                'icon': '🎨',
                'description': 'Unique and user-friendly designs that enhance user experience and brand identity.'
            }
        ]
    }
    return render(request, 'about_us/about_us.html', context)


def darslar(request):
    return render(request, 'about_us/darslar.html')
