import sys
import re

with open('d:/Freelance/mclean_project/templates/services/service_detail.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove Pricing Section
text = re.sub(r'<!-- PRICING SECTION -->.*?</section>\n', '', text, flags=re.DOTALL)

# 2. Extract sections
portfolio_match = re.search(r'<!-- RELATED PORTFOLIO -->.*?</section>\n(?:{% endif %}\n)?', text, flags=re.DOTALL)
if portfolio_match:
    portfolio = portfolio_match.group(0)
    text = text.replace(portfolio, '')
else:
    print('Portfolio not found')

partners_match = re.search(r'{% if partners %}\n<!-- PARTNERS SECTION -->.*?</section>\n{% endif %}\n', text, flags=re.DOTALL)
if partners_match:
    partners = partners_match.group(0)
    text = text.replace(partners, '')
else:
    print('Partners not found')

recommended_match = re.search(r'<section class=\"section section--green\">\s*<div class=\"container\">\s*<div class=\"section__header fade-in\">\s*<h2 class=\"section__title\">Вас также может заинтересовать.*?</section>\n', text, flags=re.DOTALL)
if recommended_match:
    recommended = recommended_match.group(0)
    text = text.replace(recommended, '')
else:
    print('Recommended not found')

blog_match = re.search(r'<!-- BLOG SECTION -->.*?</section>\n(?:{% endif %}\n)?', text, flags=re.DOTALL)
if blog_match:
    blog = blog_match.group(0)
    text = text.replace(blog, '')
else:
    print('Blog not found')

# Now insert them where they belong.
# Partners AFTER Portfolio
if portfolio_match and partners_match:
    combined_portfolio_partners = portfolio + '\n' + partners
    # insert before FAQ
    text = text.replace('<!-- FAQ SECTION -->', combined_portfolio_partners + '\n\n<!-- FAQ SECTION -->')
else:
    print("Could not combine portfolio and partners")
        
# Recommended BEFORE Blog
if recommended_match and blog_match:
    combined_rec_blog = recommended + '\n' + blog
    text = text.replace("{% include 'includes/partner_modal.html' %}", combined_rec_blog + '\n{% include \'includes/partner_modal.html\' %}')
else:
    print("Could not combine recommended and blog")

with open('d:/Freelance/mclean_project/templates/services/service_detail.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
